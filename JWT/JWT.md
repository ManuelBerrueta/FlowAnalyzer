# JSON Web Tokens aka `JWT`(s) aka JAWTs
As mentioned in the `/README.md` file, JWTs are the token type that OAuth uses. What that really means, is that each time we execute a flow and request a token in OAuth, we will get back a JWT for all three types of security tokens (`id_token`, `access_token`, `refresh_token`).

## The Three Components of a JSON Web Token
There are three components to a JWT:
1. **Header**
2. **Payload**
3. **Signature**.

The three components are separated by a dot "**`.`**" character, which looks like this `{Header}.{Payload}.{Signature}`.   
   
Further, each of the three components is base64url encoded to make it safe to travel the interwebs, because bas64 is a proven method to transfer data using the HTTP protocol. Base64 helps deliver special characters and binary data which HTTP may not agree with directly.   
   
The first 2 components are JSON objects containing the necessary information to identify how to handle the token via the **`Header`**, while the **`Payload`** contains the `Claims` contain critical data that allow the application to perform it's duties. Last but not least, the third component is the signature calculated most often by the IdP.

### Header
The header is a JSON object that typically includes two parts:
- `alg`: The signing algorithm being used (e.g., `HS256` for **`HMAC SHA-256`** or `RS256` for **``RSA SHA-256``** ).
- `typ`: The type of token, which is JWT.

It looks like so:
```JSON
{
  "alg": "RS256",
  "typ": "JWT"
}
```

### Payload
As mentioned before the **Payload** contains a JSON object with all the **`claims`**.
The **`claims`** help identify the user/application which includes data such as who issued the token, who is the intended recipient for the token, what resource the token is for and other useful things that allow the application to perform it's duties.

A brief example:
```JSON
{
  "sub": "1234567890",
  "name": "John Doe",
  "admin": true
}
```

### Signature
1. To calculate the signature, we must first base64url encode the `Header` and the `Payload` independently and then concatenate them with the dot **`.`** as a separator.

2. The combined string is signed using a secret key with the specified signing algorithm (e.g., HMAC SHA-256).
which is derived by using the information from the `Header`, specifically the **`alg`** component, which most often is `RS256`. 

---    
## Signing Process
### RS256

### HS256
- **HMAC (Hash-Based Message Authentication Code)**: It's a mechanism that combines a cryptographic hash function (like SHA-256) with a secret key. It provides both data integrity and authentication.
- **HMAC Function Name**: When using HMAC with SHA-256, the function is often referred to as HMAC-SHA256.

#### The HMAC process involves:
1. The combined header and payload string is hashed using SHA-256, this is called the "message".
2. The message is then signed using the secret/private key
3. The result is binary data, which then get's base64url encoded
4. Finally, the signature get's concatenated after the `Payload` with the dot **`.`** separator, like the other two JWT components before.

---    
## Security Considerations
### Why do we go through all this trouble of signing?
There are a few reasons, one is to make sure that the token (most specifically the claims) has not been tampered with and another is to verify that it was signed by the IdP we expect. As the signature is verified it performs both of those things.

### Signature Algorithm Security Considerations
#### RS256 (Asymmetric Algorithm)
- Key Management: Asymmetric algorithms like RSA involve managing a key pair. The private key must be securely stored, while the public key can be distributed.
- Public Key Distribution: The public key must be shared with all entities that need to verify the JWT signature. This allows easy verification without exposing the private key.
- Scalability: Easier to manage in distributed systems where multiple services need to verify the JWT, as they only need the public key.

#### HMAC-SHA256 (Symmetric Algorithm)
- Key Management: Symmetric algorithms use a single key that must be kept secret and securely shared between all parties.
- Key Distribution: All parties that need to sign or verify the JWT must have access to the shared secret key, increasing the risk of key exposure.
- Scalability: Can be less scalable in large systems because the same secret key must be securely distributed and managed across all verifying parties.

---    
### RFC 7519
If you want to learn further about the low level implementation of JSON Web Tokens (JWT), check out the spec: [RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519)

---    
#### Reference
- [revx0r.com: JWT Tokens...](https://www.revx0r.com/2021/12/30/jwt-tokens-index.html): I used my JWT blog post as a starting point for this information.

#### Other Resources
- [jwt.ms](https://jwt.ms/): JWT decoding tool from MS
- [jwt.io](https://jwt.io/): A 3rd party JWT decoder tool
- [BST](https://github.com/ManuelBerrueta/BST): Includes a compilation of tools, but the `/JWT_Utils` directory contains some useful ones for signing & decoding JWTs.
