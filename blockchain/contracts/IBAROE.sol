// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IBAROE {
    struct RegulatoryRecord {
        uint256 id;
        string description;
        uint256 timestamp;
        address submitter;
    }

    RegulatoryRecord[] public records;
    uint256 public recordCount;

    event RecordAdded(uint256 indexed id, string description, uint256 timestamp, address submitter);

    function addRecord(string memory _description) public {
        recordCount++;
        records.push(RegulatoryRecord(recordCount, _description, block.timestamp, msg.sender));
        emit RecordAdded(recordCount, _description, block.timestamp, msg.sender);
    }

    function getRecord(uint256 _id) public view returns (uint256, string memory, uint256, address) {
        require(_id > 0 && _id <= recordCount, "Invalid record ID");
        RegulatoryRecord memory record = records[_id - 1];
        return (record.id, record.description, record.timestamp, record.submitter);
    }

    function getRecordCount() public view returns (uint256) {
        return recordCount;
    }
}