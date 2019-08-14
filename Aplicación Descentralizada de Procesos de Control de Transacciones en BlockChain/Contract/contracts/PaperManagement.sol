pragma solidity >=0.4.21 <0.6.0;

import "./Ownable.sol";
import "./UserManagement.sol";

contract PaperManagement is Ownable, UserManagement{

    struct infoPaper{
        bool exists;
        string issue;
        string authors;
        string title;
        string username;
    }

    mapping(bytes32 => infoPaper) paperByContent;
    //The paper ID will be the position of its content in the below array.
    bytes32[] contentList;

    event PaperStored(string indexed _authors, string indexed _title);

    function storePaper(bytes32 _paperContent,
                        string memory _issue,
                        string memory _authors,
                        string memory _title,
                        string memory _username) public
                        onlyOwner
                        registeredUser(_username) {
        require(!paperByContent[_paperContent].exists, "This paper is already lodaded");
        infoPaper memory newPaper = infoPaper(true,
                                              _issue,
                                              _authors,
                                              _title,
                                              _username);
        contentList.push(_paperContent);
        paperByContent[_paperContent] = newPaper;
        emit PaperStored(_authors, _title);
    }

    function getPaperById(uint _idPaper) public view returns(
        string memory issue,
        string memory authors,
        string memory title,
        string memory username,
        bytes32 content
    ){
        content = contentList[_idPaper];
        infoPaper memory paper = paperByContent[content];
        authors = paper.authors;
        title = paper.title;
        issue = paper.issue;
        username = paper.username;
    }

    function getPaperByContent(bytes32 _content) public view returns(
        string memory issue,
        string memory authors,
        string memory title,
        string memory username
    ){
        infoPaper memory paper = paperByContent[_content];
        issue = paper.issue;
        authors = paper.authors;
        title = paper.title;
        username = paper.username;
    }

    function papersCount() public view returns (uint){
        return contentList.length;
    }

    function getLastID() public view returns(uint){
        uint count = this.papersCount();
        if(count > 0) count--;
        return count;
    }

}
