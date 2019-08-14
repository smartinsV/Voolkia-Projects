from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from web3 import Web3
from eth_account import Account
import json
import binascii

from flask_cors import CORS

# Ganache GUI 
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

app = Flask(__name__)
# CORS ONLY FOR DEVELOPMENT
# cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

#FROM GANACHE GUI 
private_key = '520253a4c6cf518fe8863d662d26139ac06e3b8760e03c0fbb494a5effa6684e'
account = Account.privateKeyToAccount(private_key)

# CONTRACT config
CONTRACT_ADDR = '0x51121d4632647Bb828F7B10D5AD3633b75316F29'
CONTRACT_ABI = json.loads("""[
  {
    "constant": true,
    "inputs": [
      {
        "name": "_username",
        "type": "string"
      },
      {
        "name": "_password",
        "type": "string"
      }
    ],
    "name": "checkUserData",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0x31b022d0"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_username",
        "type": "string"
      },
      {
        "name": "_name",
        "type": "string"
      },
      {
        "name": "_lastName",
        "type": "string"
      },
      {
        "name": "_email",
        "type": "string"
      },
      {
        "name": "_password",
        "type": "string"
      }
    ],
    "name": "createUser",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function",
    "signature": "0x65c06f70"
  },
  {
    "constant": false,
    "inputs": [],
    "name": "renounceOwnership",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function",
    "signature": "0x715018a6"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "owner",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0x8da5cb5b"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "isOwner",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0x8f32d59b"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "newOwner",
        "type": "address"
      }
    ],
    "name": "transferOwnership",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function",
    "signature": "0xf2fde38b"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "_authors",
        "type": "string"
      },
      {
        "indexed": true,
        "name": "_title",
        "type": "string"
      }
    ],
    "name": "PaperStored",
    "type": "event",
    "signature": "0x25e62903523bb2d8b5ac0a57d502eacf7ffdec19a7a0dd0ce796fcacbfef54a2"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "previousOwner",
        "type": "address"
      },
      {
        "indexed": true,
        "name": "newOwner",
        "type": "address"
      }
    ],
    "name": "OwnershipTransferred",
    "type": "event",
    "signature": "0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_paperContent",
        "type": "bytes32"
      },
      {
        "name": "_issue",
        "type": "string"
      },
      {
        "name": "_authors",
        "type": "string"
      },
      {
        "name": "_title",
        "type": "string"
      },
      {
        "name": "_username",
        "type": "string"
      }
    ],
    "name": "storePaper",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function",
    "signature": "0xb2887996"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_idPaper",
        "type": "uint256"
      }
    ],
    "name": "getPaperById",
    "outputs": [
      {
        "name": "issue",
        "type": "string"
      },
      {
        "name": "authors",
        "type": "string"
      },
      {
        "name": "title",
        "type": "string"
      },
      {
        "name": "username",
        "type": "string"
      },
      {
        "name": "content",
        "type": "bytes32"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0x3e0b7810"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_content",
        "type": "bytes32"
      }
    ],
    "name": "getPaperByContent",
    "outputs": [
      {
        "name": "issue",
        "type": "string"
      },
      {
        "name": "authors",
        "type": "string"
      },
      {
        "name": "title",
        "type": "string"
      },
      {
        "name": "username",
        "type": "string"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0x73e4b65b"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "papersCount",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0x916cec76"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "getLastID",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function",
    "signature": "0x12ba91ea"
  }
]""")
CONTRACT_INSTANCE = w3.eth.contract(address=CONTRACT_ADDR, abi=CONTRACT_ABI)

# parser = reqparse.RequestParser()

class PublicationList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user') # string
    parser.add_argument('content') # string
    parser.add_argument('vol') # string
    parser.add_argument('authors') # string
    parser.add_argument('title') # string
    #TODO: ADD PARSER FOR OTHER

    def get(self):
        count = CONTRACT_INSTANCE.functions.papersCount().call()
        publications = {}
        for id in range(count):
            [vol, author, title, user, content] = CONTRACT_INSTANCE.functions.getPaperById(id).call()
            publications[str(id)] = {
                "volume": vol, 
                "authors": author,
                "title": title,
                "user": user,
                "content_hash": str(binascii.hexlify(content))
            }
        return publications
    
    def post(self):
      # aca se guarda el paper 
      args = self.parser.parse_args()
      nonce = w3.eth.getTransactionCount(account.address)
      pm_txn = CONTRACT_INSTANCE.functions.storePaper(args.content, 
                                                      args.vol,
                                                      args.authors, 
                                                      args.title, 
                                                      args.user).buildTransaction({
                                                          "nonce": nonce,
                                                      })
      signed_txn = w3.eth.account.signTransaction(pm_txn, private_key=private_key)
      txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
      receipt = w3.eth.waitForTransactionReceipt(txn_hash)
      print(receipt)
      if(receipt.status) :
        code = 201
      else: 
        code = 409
      return {"receipt" : f'0x{str(binascii.hexlify(txn_hash))}'}, code

class Publication(Resource):
    def get(self, publication_id):
        [vol, author, title, user, content]\
             = CONTRACT_INSTANCE.functions.getPaperById(int(publication_id)).call()
        return {
            "volume": vol, 
            "authors": author,
            "title": title,
            "user": user,
            "content_hash": str(binascii.hexlify(content))
        }


class PaperByContent(Resource):
    def get(self, content):
        [vol, author, title, user] = \
            CONTRACT_INSTANCE.functions.getPaperByContent(content).call()
        return {
            "volume": vol, 
            "authors": author,
            "title": title,
            "user": user,
        }

class Count(Resource):
    def get(self):
        return {"count": CONTRACT_INSTANCE.functions.papersCount().call()}

##
## Actually setup the Api resource routing here
##
RESOURCES = [
  (PublicationList, '/publications'),
  (Publication, '/publications/<publication_id>'),
  (Count, '/publications/count'),
  (PaperByContent, '/publications/content/<content>'),
]

for resource,endpoint in RESOURCES:
  api.add_resource(resource, endpoint)


if __name__ == '__main__':
    app.run(debug=True)
