function Table({ data, columns }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-sm border-separate border-spacing-y-3">
        <thead>
          <tr className="text-slate-400">
            {columns.map((column, index) => (
              <th key={index} className="pb-3">
                {column.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex} className="border-t border-slate-800">
              {columns.map((column, colIndex) => (
                <td key={colIndex} className="py-3 text-slate-200">
                  {column.render ? column.render(row[column.key], row) : row[column.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Table