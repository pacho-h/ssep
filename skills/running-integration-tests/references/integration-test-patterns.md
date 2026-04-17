# Integration Test Patterns

Patterns for HTTP + DB integration tests. Specifics depend on the project's framework (NestJS, Express, FastAPI, Django, etc.) but the patterns generalize.

## Test database setup

Two viable approaches:

### Option A: shared test DB with transactional rollback
Each test runs inside a transaction that rolls back at teardown. Fast (no schema setup per test), but requires the framework to support nested transactions (most ORMs do via savepoints).

```
beforeEach: BEGIN
test runs against the connection in the transaction
afterEach: ROLLBACK
```

Pros: fast, isolated.
Cons: tests that themselves use transactions interact awkwardly with the wrapping transaction.

### Option B: ephemeral test DB per test file
A new DB is created per test file (or test suite), schema applied, dropped at teardown. Slower setup but gives full freedom inside tests.

Pros: real transactions in tests work normally.
Cons: slower; needs DB creation/teardown infrastructure.

Choose A unless tests need to verify transactional behavior; in that case choose B.

## Fixture data

Two strategies:

- **Programmatic factories:** call `createUser()`, `createOrder()` helpers that return realistic objects. Best for tests where the data is incidental to what's being tested.
- **Inline minimal data:** hand-write the few rows needed. Best for tests where the exact data shape *is* the test.

Avoid: large shared fixture files. They couple tests to each other and obscure what each test depends on.

## Request helpers

Wrap the HTTP framework's test client into a small helper that:
- Authenticates as a user identity (real auth flow, not mocked tokens — testing auth is part of integration testing)
- Returns parsed body alongside status
- Throws with full response context on assertion failure (status + headers + body, not just "expected 200 got 500")

## Common pitfalls

- **Mocking the DB.** Tests pass; production breaks because the mock didn't enforce the constraint.
- **Hardcoding IDs.** Tests fail when run in parallel or in different order. Use factory-generated IDs.
- **Skipping cleanup.** Test pollution makes failures depend on prior test state — non-deterministic and impossible to debug.
- **Asserting on log lines.** Logs are an implementation detail; refactors break tests.
- **Forgetting the test runs against test data.** A test that asserts "user count > 0" passes accidentally because seed data exists; it would fail on a clean DB. Assert on state created by the test itself.

## Skeleton (NestJS + MikroORM example, adapt for project)

```typescript
describe('GET /api/orders (integration)', () => {
  let app: INestApplication;
  let em: EntityManager;

  beforeAll(async () => {
    app = await createTestApp();
    em = app.get(EntityManager);
  });
  afterAll(() => app.close());

  beforeEach(async () => { await em.begin(); });
  afterEach(async () => { await em.rollback(); });

  it('returns the requesting user\'s orders, newest first', async () => {
    const user = await createUser(em);
    const _other = await createUser(em);
    await createOrder(em, { user, createdAt: new Date('2025-01-01') });
    await createOrder(em, { user, createdAt: new Date('2025-02-01') });
    await createOrder(em, { user: _other }); // should not appear

    const res = await request(app.getHttpServer())
      .get('/api/orders')
      .auth(...userToken(user));

    expect(res.status).toBe(200);
    expect(res.body.items).toHaveLength(2);
    expect(res.body.items[0].createdAt).toBe('2025-02-01T00:00:00.000Z');
  });
});
```
