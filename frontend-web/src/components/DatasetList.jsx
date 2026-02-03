const DatasetList = ({ datasets, selected, onSelect }) => {
    if (datasets.length === 0) {
        return (
            <p className="px-3 text-sm text-slate-500 italic">No datasets uploaded yet</p>
        );
    }

    const getStatusColor = (index) => {
        const colors = ['bg-green-500', 'bg-yellow-500', 'bg-blue-500', 'bg-purple-500', 'bg-red-500'];
        return colors[index % colors.length];
    };

    return (
        <div className="space-y-1">
            {datasets.map((dataset, index) => (
                <button
                    key={dataset.id}
                    onClick={() => onSelect(dataset)}
                    className={`
            w-full group flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-left transition-all
            ${selected?.id === dataset.id
                            ? 'bg-primary/20 text-white border border-primary/30'
                            : 'text-slate-400 hover:text-white hover:bg-white/5'
                        }
          `}
                >
                    <span className={`w-1.5 h-1.5 rounded-full ${getStatusColor(index)} shadow-[0_0_5px_currentColor]`}></span>
                    <span className="truncate flex-1">{dataset.name}</span>
                    <span className="text-xs text-slate-500">{dataset.total_count}</span>
                </button>
            ))}
        </div>
    );
};

export default DatasetList;
