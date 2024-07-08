# Creating a certificate
To create a certificate we must first create the key and a certificate signing request (CSR):
```Shell
openssl req -newkey rsa:4096 -nodes -keyout flow_analyzer.key -batch -out flow_analyzer.csr
```

Now we can self sign our certificate:
```Shell
openssl x509 -key flow_analyzer.key -in flow_analyzer.csr -req -days 3650 -out flow_analyzer.crt
```

- Now we need to upload the certificate to the App Registration
- We will be using the key to sign the **`client_assertion`** JWT.

---     
# Signing in with the certificate
To now use the certificate for authentication, you will need to calculate the **`x5t`** parameter. The `x5t_Calculation.ipynb` notebook walks you through that.
