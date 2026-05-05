# Enforcing signed commits on the publish workflow

The Docker publish workflow (`docker-publish.yml`) triggers on any `v*` tag push.
To ensure only commits signed by a trusted key can produce a published image, there
are two complementary layers.

## Layer 1 — GitHub repository ruleset (most effective)

Enforced *before* a push is accepted, so an unsigned tag is rejected outright and
the workflow never fires.

1. Go to **Settings → Rules → Rulesets** in the GitHub repository.
2. Create a new ruleset targeting **tag** refs matching the pattern `v*`.
3. Enable **Require signed commits**.

GitHub recognises SSH signing keys, but they must be registered separately from
authentication keys: **Settings → SSH and GPG keys → Signing keys**.

> If you sign with `git config gpg.format ssh`, make sure the key listed under
> `user.signingKey` in your git config is the one registered there.

## Layer 2 — Verification step in the workflow (defense-in-depth)

Even with a ruleset in place, an early step in the workflow can assert that the
triggering commit is marked as verified by GitHub before any Docker work begins.
This catches edge cases where the ruleset is misconfigured or temporarily bypassed
by a repository admin.

```yaml
- name: Verify commit signature
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    verified=$(gh api repos/${{ github.repository }}/commits/${{ github.sha }} \
      --jq '.commit.verification.verified')
    if [ "$verified" != "true" ]; then
      echo "Commit is not signed or not verified by GitHub. Aborting."
      exit 1
    fi
```

Add this as the first step in the `build-and-push` job, before the checkout step.

## Which layers to use

| Scenario | Recommendation |
|---|---|
| Personal repo, sole maintainer | Layer 1 alone is sufficient |
| Multiple maintainers or higher assurance | Both layers |

Layer 2 alone has a gap: the workflow runner starts and checks out code before the
verification runs. It would stop before pushing an image, but the workflow has
already consumed runner time and checked out the repository.

## Prerequisite checklist

- [ ] SSH public key added as a **signing** key on GitHub (not just an auth key)
- [ ] Local git config: `gpg.format = ssh`
- [ ] Local git config: `user.signingKey = /path/to/your/public/key.pub`
- [ ] Test with `git log --show-signature` to confirm commits are signed locally
- [ ] Push a signed commit and verify it shows **Verified** on GitHub before enabling the ruleset
