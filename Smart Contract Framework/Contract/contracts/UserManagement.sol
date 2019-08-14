pragma solidity >=0.4.21 <0.6.0;
import "./Ownable.sol";

contract UserManagement is Ownable{

    struct user{
        bool set;
        //TODO: hash password
        string password;
        string name;
        string lastName;
        string email;
    }

    mapping(string => user) users;

    function createUser(string memory _username,
                        string memory _name,
                        string memory _lastName,
                        string memory _email,
                        string memory _password) public onlyOwner {
        require(!users[_username].set, "User already exists");
        user memory newUser = user(true,
                                   _password,
                                   _name,
                                   _lastName,
                                   _email);
        users[_username] = newUser;
    }

    modifier registeredUser(string memory _username) {
        require(users[_username].set, "User not registered");
        _;
    }

    function checkUserData(string memory _username, string memory _password)
        public view returns(bool) {
        return (keccak256(abi.encodePacked((users[_username].password))) == keccak256(abi.encodePacked((_password))));
    }
}