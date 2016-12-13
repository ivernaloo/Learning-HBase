var assert = require('assert');
var hbase = require('hbase');
var client = hbase({ host: 'localhost', port: 16010 });
var test = hbase({ host: '192.168.99.100', port: 32770 });

// 列出所有的表
test.tables(function(err, tables){
    console.log("已经有的表",tables);
});

var testTable = test.table('test');

testTable.exists(function(err, exists){
    
});

testTable.create(function(err, suc){
    console.log("err : ", err);
    console.log("suc : ", suc);
});

// 创建table

// 插入数据

// 读取数据

// test.table('test').row().put([
//     {
//         key: 'test_filter|row_1',
//         column: 'node_column_family:aa',
//         $: 'aa'
//     }, {
//         key: 'test_filter|row_1',
//         column: 'node_column_family:aa',
//         $: 'ab'
//     }, {
//         key: 'test_filter|row_1',
//         column: 'node_column_family:aa',
//         $: 'ac'
//     }, {
//         key: 'test_filter|row_2',
//         column: 'node_column_family:ab',
//         $: 'ba'
//     }, {
//         key: 'test_filter|row_2',
//         column: 'node_column_family:bb',
//         $: 'bb'
//     }, {
//         key: 'test_filter|row_2',
//         column: 'node_column_family:bc',
//         $: 'bc'
//     }, {
//         key: 'test_filter|row_3',
//         column: 'node_column_family:ca',
//         $: 'cc'
//     }, {
//         key: 'test_filter|row_3',
//         column: 'node_column_family:cb',
//         $: 'cc'
//     }, {
//         key: 'test_filter|row_3',
//         column: 'node_column_family:cc',
//         $: 'cc'
//     }
// ], function(err, success) {
//     console.log("err : ", err)
//     console.log("success : ", success)
// })