---
type: llm
weight: 1
---

Pass if this holds for the response: The response identifies that sending the new `partially_refunded` value to existing app versions will make their strict enum decoding fail (Swift Codable and Moshi's default enum adapter reject unknown values), which can break decoding of the whole order or order list — i.e. adding an enum value is a breaking change for these clients.
