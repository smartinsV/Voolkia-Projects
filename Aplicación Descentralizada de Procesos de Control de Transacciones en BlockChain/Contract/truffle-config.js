var HDWalletProvider = require('truffle-hdwallet-provider')

var mnemonic = 'require clean disagree emotion choose license clever property motion warrior mask faint'
var publicNode = 'https://public-node.testnet.rsk.co:443'

module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // for more about customizing your Truffle configuration!
  networks: {
    development: {
      host: "127.0.0.1",
      port: 8545,
      network_id: "*" // Match any network id
    },
    rsk: {
      provider: () =>
        new HDWalletProvider(mnemonic, publicNode),
      network_id: '*',
      gas: 2500000,
      gasPrice: 183000
    }
  }
};
