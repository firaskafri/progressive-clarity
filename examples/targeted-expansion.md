# Targeted expansion

- **Expected views:** At a glance on the parent topic, then In context on the invalidation branch only. The parent remains At a glance.
- **Required facts at first stop:** Use a staged rollout; retain rollback; stale results are the primary risk.
- **Required additions for the branch:** Describe the fill race, a prevention mechanism, required tests, and a freshness alert.
- **Budget:** The branch inherits the parent topic's count. At a glance is at most 40 counted words, and parent plus branch prose through In context is at most 200 words.

## Initial prompt

How should we roll out caching for search results?

## Assistant — At a glance

<!-- words:targeted-glance:start -->
Use a staged rollout with request coalescing and a rollback switch. The main operational risk is stale results, so production activation depends on verified invalidation and freshness monitoring.
<!-- words:targeted-glance:end -->

## User

Expand only the invalidation risk.

## Assistant — In context on the selected branch

<!-- words:targeted-context:start -->
**Keep in view:** Writes can race with cache fills, allowing an older value to overwrite a fresh invalidation. Version cache entries or compare write timestamps before storing fills. Test delete, update, and partial-failure paths; alert on age, not only hit rate.
<!-- words:targeted-context:end -->
