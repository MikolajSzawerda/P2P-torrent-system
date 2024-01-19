```json
{
  "hash": "abcde",
  "fragment": 0
}
```

Client-Client(binary)

```yaml
type: [ 0|1 ]
length: 0 # Length of data carrying
fragment_id: 1024 # Id of fragment as request/transfer
hash: ajdf324j # Optional, used during transfer
data: # Binary content of file
  - [ ]
```