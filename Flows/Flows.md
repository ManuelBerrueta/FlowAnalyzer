# OAuth 2.0 Flows Overview:    
OAuth 2.0 is an **authorization** protocol, but extending the protocol's functionality using OpenID Connect (OIDC) allows for **authentication** as well. 
Below is a brief overview of each flow. For more details and execution steps, refer to the specific directories for each flow.

> [!NOTE] If you are interested in digging further into the spec, check out [**RFC 6749**](https://datatracker.ietf.org/doc/html/rfc6749).


## Authorization Code Grant Flow    
This flow is used to acquire an Authorization Code (`auth_Code`) from the **`/authorize`** endpoint with the desired scope, which the user must first login (authentication) and consent to (authorization). 
    
The application will then need to redeem this `auth_code` for an `access_token` by making a request to the **`/token`** endpoint providing the `auth_code` and it's `client_secret`.    
    
Putting it all together: Once having an `access_token`, the application can access the resource(s) it was given permission to via the `scope` in the original request.

> [!NOTE] 💡 Auth Code Flow provides a secure, two-step process for obtaining tokens; best for server-side applications.

## Auth Code Grant Flow with PKCE
The `/Flows/Auth_Code_Flow/Auth_Code_wCert_Flow.ipynb` has an example on how to use the Auth Code Grant with PKCE

### Hybrid Flow - OpenID Connect
The Hybrid Flow extends the Authorization Code Grant Flow to be able to request both **`id_token`** and **`access_token`**. The **`access_token`** support is meant to be used as a more secure implicit flow replacement.

> [!NOTE] 💡 Combines immediate token access with secure authorization code exchange; flexible for applications needing quick authentication and secure authorization.

> [!NOTE] 📝 An insightful nuance here is that you are able to request any combination of the 3 (as long as it has been enabled in the App registrations): [`id_token`, `access_token`, `auth_code`]

#### Requirements to be able to request an `id_token`    
Note that in your specific App in App registrations -> Authentication, under "Implicit grant and hybrid flows", you must enable "**ID tokens (used for implicit and hybrid flows)**" or else the flow will fail.

#### Requirements to be able to request an `access_token`    
Note that in your specific App in App registrations -> Authentication, under "Implicit grant and hybrid flows", you must enable "**Access tokens (used for implicit flows)**" or else the flow will fail.

---   
### Refresh Tokens
The `refresh_token` examples are included within the Auth Code Flow and the Hybrid Flow.

---    
## Client Credentials Grant Flow
Uses the App's credentials to login, instead of a user's credentials. Most often used in Server-To-Server or Service-To-Service (STS) scenarios.

---   
## Device Code Flow 
This flow is used mainly for Internet connected devices that may not have a browser or are input constrained. 

---    
## On-Behalf-Of (OBO) Flow 
On-Behalf-Of (OBO) Flow is used for service-to-service (server-to-server) communication where an API A need access to API B.
- Supports requesting token for APIs that require SAML tokens

---    
## Implicit Grant Flow
The key feature of the implicit grant is that tokens (ID or access) are returned directly from the `/authorize` endpoint instead of the `/token` endpoint.

---    
## Resource Owner Password Credentials (ROPC) Grant Flow
In this flow, the client application directly handles the user's credentials, instead of the IDP.
- 🛑 Not the most secure and certainly not recommended to use if you can use an alternative flow.
- ❌ This flow has quite a few limitations, visit the notebook for more info.

---     
# Certificate Auth & Setup
For Certificate Authentication check out the **`Cert_Setup`** directory with instructions on how to set that up, create a token and signing it.
The `Auth_Code_Flow` directory has an example Notebook using the certificate authentication that you can use with the other flows.

---    
# Error Checking
If you have an error code in the response you can use this endpoint to check the error's code meaning: `https://login.microsoftonline.com/error`. 
Here is an example using the code query string using the 70016 as the code value: `https://login.microsoftonline.com/error?code=70016`.
