const DatasetList = ({ datasets, selected, onSelect }) => {
    if (datasets.length === 0) {
        return (
            <p className="px-3 text-sm text-slate-500 italic">No datasets uploaded yet</p>
        );
    }

    // Green dot for currently selected/viewing, gray for others
    const getIndicatorColor = (datasetId) => {
        return selected?.id === datasetId ? 'bg-green-500' : 'bg-slate-500';
    };

    return (
        <div className="space-y-1">
            {datasets.map((dataset, index) => {
                // Format upload date for tooltip
                const uploadDate = dataset.uploaded_at
                    ? new Date(dataset.uploaded_at).toLocaleString()
                    : 'Unknown date';
                const tooltipText = `${dataset.name}\nUploaded: ${uploadDate}`;

                return (
                    <button
                        key={dataset.id}
                        onClick={() => onSelect(dataset)}
                        title={tooltipText}
                        className={`
                w-full group flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-left transition-all
                ${selected?.id === dataset.id
                                ? 'bg-primary/20 text-white border border-primary/30'
                                : 'text-slate-400 hover:text-white hover:bg-white/5'
                            }
              `}
                    >
                        <span className={`w-1.5 h-1.5 rounded-full ${getIndicatorColor(dataset.id)} shadow-[0_0_5px_currentColor]`}></span>
                        <span className="truncate flex-1">{dataset.name}</span>
                        <span className="text-xs text-slate-500">{dataset.total_count}</span>
                    </button>
                );
            })}
        </div>
    );
};

export default DatasetList;
