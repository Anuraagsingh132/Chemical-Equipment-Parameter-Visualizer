const EquipmentTable = ({ equipment }) => {
    if (!equipment || equipment.length === 0) {
        return (
            <div className="glass-card rounded-xl p-8 text-center">
                <span className="material-symbols-outlined text-4xl text-slate-600 mb-2">table_rows</span>
                <p className="text-slate-400">No equipment data available</p>
            </div>
        );
    }

    const getTypeIcon = (type) => {
        const icons = {
            'Reactor': 'propane_tank',
            'Pump': 'cyclone',
            'Valve': 'valve',
            'Heat Exchanger': 'heat',
            'Column': 'view_column',
            'Separator': 'filter_alt',
        };
        return icons[type] || 'settings';
    };

    // Status logic based on temperature thresholds (explained in documentation)
    // Active: temperature < 90°C (normal operating range)
    // Warning: temperature 90-150°C (elevated, needs monitoring)
    // Offline: temperature > 150°C (critical, requires attention)
    const getStatusBadge = (equipment) => {
        const temp = equipment.temperature || 0;
        if (temp > 150) {
            return {
                label: 'Offline',
                bgColor: 'rgba(100, 116, 139, 0.1)',      // slate
                textColor: '#94a3b8',                     // slate-400
                borderColor: 'rgba(100, 116, 139, 0.2)',
                dotColor: '#64748b'                       // slate-500
            };
        } else if (temp >= 90) {
            return {
                label: 'Warning',
                bgColor: 'rgba(245, 158, 11, 0.1)',       // amber
                textColor: '#fbbf24',                     // amber-400
                borderColor: 'rgba(245, 158, 11, 0.2)',
                dotColor: '#f59e0b'                       // amber-500
            };
        } else {
            return {
                label: 'Active',
                bgColor: 'rgba(34, 197, 94, 0.1)',        // green
                textColor: '#4ade80',                     // green-400
                borderColor: 'rgba(34, 197, 94, 0.2)',
                dotColor: '#22c55e'                       // green-500
            };
        }
    };

    return (
        <div className="glass-card rounded-xl overflow-hidden flex flex-col">
            <div className="p-6 border-b border-glass-border flex justify-between items-center">
                <h3 className="text-lg font-bold text-white">Live Monitoring</h3>
                <span className="text-xs font-medium text-primary hover:text-blue-400 transition-colors cursor-pointer">
                    View All Report
                </span>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-white/5 text-xs text-slate-400 uppercase tracking-wider">
                            <th className="px-6 py-4 font-semibold">ID</th>
                            <th className="px-6 py-4 font-semibold">Equipment Name</th>
                            <th className="px-6 py-4 font-semibold">Type</th>
                            <th className="px-6 py-4 font-semibold text-right">Flowrate</th>
                            <th className="px-6 py-4 font-semibold text-right">Pressure</th>
                            <th className="px-6 py-4 font-semibold text-right">Temperature</th>
                            <th className="px-6 py-4 font-semibold text-center">Status</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-glass-border text-sm">
                        {equipment.map((item, index) => {
                            const status = getStatusBadge(item);
                            return (
                                <tr key={item.id} className="group hover:bg-white/5 transition-colors">
                                    <td className="px-6 py-4 text-slate-400 font-mono">#{item.id}</td>
                                    <td className="px-6 py-4 font-medium text-white">
                                        <div className="flex items-center gap-3">
                                            <div className="h-8 w-8 rounded bg-slate-700/50 flex items-center justify-center text-slate-300">
                                                <span className="material-symbols-outlined text-[18px]">{getTypeIcon(item.equipment_type)}</span>
                                            </div>
                                            {item.name}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 text-slate-300">{item.equipment_type}</td>
                                    <td className="px-6 py-4 text-slate-300 text-right font-mono">{item.flowrate?.toFixed(1)} L/min</td>
                                    <td className="px-6 py-4 text-slate-300 text-right font-mono">{item.pressure?.toFixed(1)} Bar</td>
                                    <td className="px-6 py-4 text-slate-300 text-right font-mono">{item.temperature?.toFixed(1)} °C</td>
                                    <td className="px-6 py-4 text-center">
                                        <span
                                            className="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium border"
                                            style={{
                                                backgroundColor: status.bgColor,
                                                color: status.textColor,
                                                borderColor: status.borderColor
                                            }}
                                        >
                                            <span
                                                className="h-1.5 w-1.5 rounded-full"
                                                style={{ backgroundColor: status.dotColor }}
                                            ></span>
                                            {status.label}
                                        </span>
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default EquipmentTable;
