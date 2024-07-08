# Device Code Flow Summary:
- User Code and Device Code: The device receives a user code and device code from the authorization server.
- Separate Device Authentication: The user authenticates and grants consent on a separate device with a browser.
- Polling Mechanism: The device polls the authorization server until tokens are issued.
- Ideal for: Devices with limited input capabilities or no browser, allowing secure user authentication and authorization.

---
# Device Code Flow Visualization
This diagram illustrates the steps involved in the Device Code Flow, highlighting the interactions between the device, the authorization server, and the user (on a separate device).

```mermaid
sequenceDiagram
    participant Device
    participant Authorization Server
    participant User
    participant User Device

    Device->>Authorization Server: Request device_code and user_code
    Authorization Server-->>Device: Return device_code and user_code, verification_uri, interval
    Device->>User: Display user_code and verification_uri

    Note over User, User Device: User switches to a separate device (e.g., smartphone, computer)

    User Device->>User Device: User navigates to verification_uri
    User Device->>User Device: User enters user_code
    User Device->>Authorization Server: User authenticates and grants consent
    Authorization Server-->>User Device: Confirm authentication and consent

    loop Polling for tokens
        Device->>Authorization Server: Poll for tokens with device_code
        Authorization Server-->>Device: Authorization pending (until user authenticates)
    end

    Authorization Server-->>Device: Return access_token and id_token
    Device-->>Device: Use tokens to access resources

```