//TESTNET RSK
//let address = '0x25a4Fc2b0BB39bE28D851aC485824bB7479d0F3C'

//GANACHE - cli
// let address = '0xff6e2B1218b5c7Dc810c37a259FEd07E3F3A4a8E'

//GANACHE - gui
let address = '0x51121d4632647Bb828F7B10D5AD3633b75316F29'

if (typeof web3 !== 'undefined') {
    web3 = new Web3(web3.currentProvider);
} 
else {
    // set the provider you want from Web3.providers
    web3 = new Web3(new Web3.providers.HttpProvider('https://public-node.testnet.rsk.co:443'));
}

web3.version.getNetwork((err, netId) => {
    console.log(netId)
})

web3.eth.getAccounts((err, acc)=> {
    web3.eth.defaultAccount = acc[0];
});

let PaperManagementContract = web3.eth.contract([
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
], (err, callback) => {
        if(err) console.log(err);
    }
);

let ps = PaperManagementContract.at(address, 
    (err, resp) => {
        if(err) console.log(err);
});
