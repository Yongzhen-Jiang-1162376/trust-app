import React, { useMemo } from 'https://esm.sh/react@18';
import ReactDOM from 'https://esm.sh/react-dom@18';
import { useReactTable, getCoreRowModel } from 'https://esm.sh/@tanstack/table-core';


console.log(React)
console.log(ReactDOM)
console.log(useReactTable)

const data = [
    {name: "John", age: 30, city: "New York"},
    {name: "Jane", age: 25, city: "London"}
]

const columns = [
    {
    Header: 'Name',
    accessor: 'name' // key from the data
    },
    {
    Header: 'Age',
    accessor: 'age'
    },
    {
    Header: 'City',
    accessor: 'city'
    }
];

const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel()
})

console.log(table)

// const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = tableInstance;

const EmployeeTable = () => {
    <table>
        <thead>
            <tr>
                <th>Month</th>
                <th>Savings</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>January</td>
                <td>$100</td>
            </tr>
            <tr>
                <td>February</td>
                <td>$80</td>
            </tr>
        </tbody>
    </table>
}

// const EmployeeTable = () => {
//     <table {...getTableProps()}>
//         <thead>
//             {headerGroups.map(headerGroup => (
//             <tr {...headerGroup.getHeaderGroupProps()}>
//                 {headerGroup.headers.map(column => (
//                 <th {...column.getHeaderProps()}>{column.render('Header')}</th>
//                 ))}
//             </tr>
//             ))}
//         </thead>
//         <tbody {...getTableBodyProps()}>
//             {rows.map(row => {
//             prepareRow(row);
//             return (
//                 <tr {...row.getRowProps()}>
//                 {row.cells.map(cell => {
//                     return <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
//                 })}
//                 </tr>
//             );
//             })}
//         </tbody>
//     </table>
// }

const root = ReactDOM.createRoot(document.getElementById('employee_table'))
root.render(
    <EmployeeTable />
)

// ReactDOM.render(
//     EmployeeTable,
//     document.getElementById('employee_table')
// );