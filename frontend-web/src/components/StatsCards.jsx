const StatsCards = ({ stats, hasHistory = false }) => {
    if (!stats) return null;

    // Trends only show if we have historical data to compare
    const cards = [
        {
            label: 'Total Equipment',
            value: stats.total_count || 0,
            unit: 'Units',
            icon: 'precision_manufacturing',
            color: 'blue',
            trend: null,
            trendLabel: 'Current dataset'
        },
        {
            label: 'Avg Flowrate',
            value: stats.avg_flowrate?.toFixed(1) || 0,
            unit: 'L/min',
            icon: 'water_drop',
            color: 'cyan',
            trend: null,
            trendLabel: 'Measured value'
        },
        {
            label: 'Sys Pressure',
            value: stats.avg_pressure?.toFixed(1) || 0,
            unit: 'Bar',
            icon: 'speed',
            color: 'purple',
            trend: null,
            trendLabel: 'Within range'
        },
        {
            label: 'Core Temp',
            value: stats.avg_temperature?.toFixed(1) || 0,
            unit: '°C',
            icon: 'thermostat',
            color: 'red',
            trend: null,
            trendLabel: 'Within range'
        }
    ];

    const colorClasses = {
        blue: {
            bg: 'bg-blue-500/10',
            text: 'text-blue-400',
            border: 'border-blue-500/20',
            glow: 'group-hover:bg-blue-500/20'
        },
        cyan: {
            bg: 'bg-cyan-500/10',
            text: 'text-cyan-400',
            border: 'border-cyan-500/20',
            glow: 'group-hover:bg-cyan-500/20'
        },
        purple: {
            bg: 'bg-purple-500/10',
            text: 'text-purple-400',
            border: 'border-purple-500/20',
            glow: 'group-hover:bg-purple-500/20'
        },
        red: {
            bg: 'bg-red-500/10',
            text: 'text-red-400',
            border: 'border-red-500/20',
            glow: 'group-hover:bg-red-500/20'
        }
    };

    return (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4 mb-6">
            {cards.map((card, index) => {
                const colors = colorClasses[card.color];
                return (
                    <div
                        key={index}
                        className="glass-card relative overflow-hidden rounded-xl p-5 hover:bg-slate-800/50 transition-colors group"
                    >
                        {/* Glow Effect */}
                        <div className={`absolute right-0 top-0 h-24 w-24 translate-x-8 -translate-y-8 rounded-full ${colors.bg} blur-2xl transition-all ${colors.glow}`}></div>

                        <div className="flex items-start justify-between">
                            <div>
                                <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">{card.label}</p>
                                <h3 className="mt-2 text-3xl font-bold text-white tracking-tight">
                                    {card.value} <span className="text-base font-normal text-slate-500 ml-1">{card.unit}</span>
                                </h3>
                            </div>
                            <div className={`flex h-10 w-10 items-center justify-center rounded-lg ${colors.bg} ${colors.text} ${colors.border} border`}>
                                <span className="material-symbols-outlined">{card.icon}</span>
                            </div>
                        </div>

                        <div className="mt-4 flex items-center gap-2 text-xs">
                            {card.trend && (
                                <span className={`flex items-center ${card.trend.includes('+') ? 'text-green-400 bg-green-500/10' : 'text-slate-400 bg-slate-700/50'} px-1.5 py-0.5 rounded`}>
                                    {card.trend.includes('+') && (
                                        <span className="material-symbols-outlined text-[14px] mr-0.5">trending_up</span>
                                    )}
                                    {card.trend}
                                </span>
                            )}
                            <span className="text-slate-500">{card.trendLabel}</span>
                        </div>
                    </div>
                );
            })}
        </div>
    );
};

export default StatsCards;
