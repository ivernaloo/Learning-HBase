var assert = require('assert');
var hbase = require('hbase');
var client = hbase({ host: 'localhost', port: 16010 });

// 列出所有的表
client.tables(function(err, tables){
    console.log(tables);
});