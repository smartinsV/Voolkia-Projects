var  PaperManagement= artifacts.require("./PaperManagement.sol");

module.exports = function(deployer) {
  deployer.deploy(PaperManagement);
};
