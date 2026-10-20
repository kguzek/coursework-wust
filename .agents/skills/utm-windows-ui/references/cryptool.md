# CrypTool 1.4.42

Tested through UTM's guest agent and an interactive desktop task. The runner
supports menu inspection/invocation; filling dialogs and saving documents still
requires a narrowly scoped helper extension.

Observed IDs (examples only; rediscover before invoking):

| Command | ID |
| --- | --- |
| Analysis → Tools for Analysis → Entropy | 33005 |
| Analysis → Tools for Analysis → Histogram | 33006 |
| Encrypt/Decrypt → Symmetric (modern) → AES (CBC) | 33013 |

## Analysis pitfalls

Verify the selected alphabet before reporting entropy. The observed default
was 26 letters, not 256 byte values. Do not report that as byte entropy or
measure HEX/Base64 text as if it were raw ciphertext.

## Verified AES round trip

From a blank state:

1. Create a new ASCII file containing `Hello CrypTool! AES test 123.` without a
   trailing newline (29 bytes). Open it through File → Open.
2. Choose Encrypt/Decrypt → Symmetric (modern) → AES (CBC).
3. In `Key Entry: Rijndael (AES)`, verify `128 bits` and enter the public test key
   `00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F`. Read it back, then Encrypt.
4. Inspect the new encryption document and Save As a fresh `ciphertext.hex`.
   The observed saved file contained 32 raw ciphertext bytes, despite `.hex` in
   its name. Do not infer file encoding from its extension.
5. With the ciphertext document active, choose AES (CBC) again, enter and verify
   the same key, and select Decrypt.
6. Inspect the decryption document, Save As a fresh `decrypted.txt`, wait for
   completion, and compare its bytes against the original. All 29 bytes matched.

Observed dialog controls (rediscover and verify before use):

| Dialog | Control | Native ID / class |
| --- | --- | --- |
| Open | File name | `1148` / `Edit` |
| Key Entry: Rijndael (AES) | Key | `1426` / `Edit` |
| Key Entry: Rijndael (AES) | Key length | `1424` / `ComboBox` |
| Key Entry: Rijndael (AES) | Encrypt | `1314` / `Button` |
| Key Entry: Rijndael (AES) | Decrypt | `1046` / `Button` |
| Save As | File name | `1001` / `Edit` |
| Save As | Save | `1` / `Button` |

The key edit accepted `WM_SETTEXT` with spaced hexadecimal text; its entered
value was readable through UI Automation even though native window text was
empty. Scintilla document text was not reliable through either inspection path.
Use saved bytes for evidence, not garbled editor names.

The key dialog did not expose an IV field; no explicit IV was set or checked.
This verifies functional recovery, not an independent AES known-answer test.
