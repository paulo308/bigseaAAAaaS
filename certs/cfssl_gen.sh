#!/bin/bash

initca() {
    ## Generate root certificate 
    cfssl genkey -initca ca_csr.json | cfssljson -bare hs_root_ca
}

mongo() {
    ## Generate ee_mongo certificate using the root
    cfssl gencert -ca root_ca.pem -ca-key root_ca-key.pem -hostname=mongo,localhost mongo_csr.json | cfssljson -bare mongo
    cat mongo-key.pem mongo.pem > mongo_crt.pem
    ## Generate ee_mongo_client certificate using the CA
    cfssl gencert -ca root_ca.pem -ca-key root_ca-key.pem -hostname=mongo,localhost mongo_client_csr.json | cfssljson -bare mongo_client
    cat mongo_client-key.pem mongo_client.pem > mongo_client_crt.pem
}



web() {
    ## Generate demo web client using the root (must be installed on browser)
    cfssl gencert -ca root_ca.pem -ca-key root_ca-key.pem web_csr.json | cfssljson -bare web
    cat web-key.pem web.pem > web_crt.pem
    cat web.pem root_ca.pem > web-bundle.pem
    openssl pkcs12 -inkey web-key.pem -in web-bundle.pem -export -out web.pfx
}

case $1 in
   "all") initca
          mongo
         ;;
   "mongo") mongo
         ;;
   "web") web
         ;;
   *) echo "Usage:    ./cfssl_gen [OPTIONS]"
        echo ""
        echo "Options:"
        echo ""
        echo "  all               Generate CA certificate, init CFSSL and generate mongo, client and web certificates"
        echo "  mongo             Generate Mongo server and client certificates"
        echo "  client            Generate client certificate"
        echo "  web               Generate web interface certificate"
        echo ""
        exit 1
        ;;
esac
