# contracts

* `black-hole`: self-destructs to itself on any transaction.
* `greeter`: returns 42; allows changing the value.
* `multisend`: performs multiple ether transfers within a single transaction call.

## Note

The `factory` contract has been moved to the [`lll-creation-patterns`][lcp]
repo and renamed to `stamping-press`.

Same goes for `cloning-vat` - it hasn't been renamed.

Sorry for the broken links! The last commit to have them is `6d7ea234`:
on [gitlab][commit] or [github][backup] (backup).

[lcp]: https://gitlab.com/veox/lll-creation-patterns
[commit]: https://gitlab.com/veox/lll-contracts/tree/6d7ea2345b21044f8b4393c25b32f2d7dfb67ec7/contracts
[backup]: https://github.com/veox/lll-contracts/tree/6d7ea2345b21044f8b4393c25b32f2d7dfb67ec7/contracts
