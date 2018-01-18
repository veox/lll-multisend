(seq
  ;; ==========================================================================
  ;; MEMORY LAYOUT

  (def '*memloc-function-selector* 0x20)
  (def '*memloc-scratchpad*        0x40)

  ;; ==========================================================================
  ;; STDLIB

  ;; --------------------------------------------------------------------------
  ;; @author Daniel Ellison <zigguratt>
  ;; @notice Shifts the leftmost 4 bytes of a 32-byte number right by 28 bytes.
  ;; @dev 0x14ab90388092664827928d90384c73d82c5bf21abb61dd7d4971fc65f4851dfb
  ;;      0x0000000000000000000000000000000000000000000000000000000014ab9038
  ;; @param input A 32-byte number.

  (def 'shift-right (input)
       (div input (exp 2 224)))

  ;; --------------------------------------------------------------------------
  ;; @author Daniel Ellison <zigguratt>
  ;; @notice Retrieves the requested function ID from the first four bytes of
  ;;         the call data.

  (def 'calldata-function-selector
       (shift-right (calldataload 0x00)))

  ;; --------------------------------------------------------------------------
  ;; @author Ben Edgington <benjaminion>
  ;; @notice Gets the function ID and stores it in memory for reference.
  ;; @dev The function ID is stored at a pre-defined location 0x20 and will
  ;;      be read from memory every time instead of duplicated on stack.
  ;; TODO: consider lll-docs lll_abi.html#passing-data-to-a-function

  (def 'mstore-function-selector
       (mstore *memloc-function-selector*
               calldata-function-selector))

  ;; --------------------------------------------------------------------------
  ;; @author Just about everybody.
  ;; @notice Convenience macro for emitting events with 1 indexed chunk.
  ;; @dev Currently does not support data longer than 32 bytes total.
  ;; @param id 32-byte event identifier.
  ;; @param indexed Data chunk that will also be indexed by in logs.
  ;; @param data Non-indexed data to be placed in logs.
  ;; @param datasize Number of bytes in data.

  (def 'emit1 (id indexed data datasize)
       (seq
         (mstore *memloc-scratchpad* data)
         (log2 *memloc-scratchpad* datasize id indexed)))

  ;; --------------------------------------------------------------------------
  ;; @author Daniel Ellison <zigguratt>
  ;; @notice Determines whether the supplied function selector matches a known
  ;;         one and executes <code-body> if so.
  ;; @dev The selector is in the leftmost four bytes of the call data:
  ;;      https://github.com/ethereum/wiki/wiki/Ethereum-Contract-ABI
  ;; @param function-hash The four-byte hash of a known function signature.
  ;; @param code-body The code to run in the case of a match.

  (def 'function (function-selector code-body)
       (when (= (mload *memloc-function-selector*) function-selector)
         code-body))

  ;; --------------------------------------------------------------------------
  ;; @author Daniel Ellison <zigguratt>
  ;; @notice Modifier macro to prevent unintended payments.

  (def 'unpayable
       (when (callvalue) (panic))))
