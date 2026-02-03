import { Bar, Doughnut } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    Title,
    Tooltip,
    Legend
);

const EquipmentChart = ({ stats }) => {
    if (!stats?.type_distribution) return null;

    const distribution = stats.type_distribution;
    const labels = Object.keys(distribution);
    const data = Object.values(distribution);
    const total = data.reduce((a, b) => a + b, 0);

    const colors = [
        '#137fec', // Primary blue
        '#06b6d4', // Cyan
        '#8b5cf6', // Purple
        '#f59e0b', // Amber
        '#10b981', // Emerald
        '#ef4444', // Red
        '#ec4899', // Pink
    ];

    const barChartData = {
        labels,
        datasets: [
            {
                label: 'Equipment Count',
                data,
                backgroundColor: colors.slice(0, labels.length),
                borderRadius: 4,
                borderSkipped: false,
            },
        ],
    };

    const barChartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: 'rgba(17, 24, 39, 0.9)',
                titleColor: '#fff',
                bodyColor: '#94a3b8',
                borderColor: 'rgba(255, 255, 255, 0.1)',
                borderWidth: 1,
                padding: 12,
                cornerRadius: 8,
            },
        },
        scales: {
            x: {
                grid: { display: false },
                ticks: { color: '#64748b', font: { size: 10 } },
            },
            y: {
                grid: { color: 'rgba(255, 255, 255, 0.05)' },
                ticks: { color: '#64748b', font: { size: 10 } },
            },
        },
    };

    const doughnutChartData = {
        labels,
        datasets: [
            {
                data,
                backgroundColor: colors.slice(0, labels.length),
                borderWidth: 0,
                hoverOffset: 4,
            },
        ],
    };

    const doughnutChartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%',
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: 'rgba(17, 24, 39, 0.9)',
                titleColor: '#fff',
                bodyColor: '#94a3b8',
                borderColor: 'rgba(255, 255, 255, 0.1)',
                borderWidth: 1,
                padding: 12,
                cornerRadius: 8,
            },
        },
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
            {/* Bar Chart */}
            <div className="glass-card lg:col-span-2 rounded-xl p-6 flex flex-col">
                <div className="flex items-center justify-between mb-6">
                    <h3 className="text-lg font-bold text-white">Equipment by Type</h3>
                </div>
                <div className="flex-1 h-64">
                    <Bar data={barChartData} options={barChartOptions} />
                </div>
            </div>

            {/* Doughnut Chart */}
            <div className="glass-card rounded-xl p-6 flex flex-col">
                <h3 className="text-lg font-bold text-white mb-6">Distribution</h3>
                <div className="flex-1 flex flex-col items-center justify-center">
                    <div className="relative h-48 w-48 mb-6">
                        <Doughnut data={doughnutChartData} options={doughnutChartOptions} />
                        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                            <span className="text-3xl font-bold text-white">{total}</span>
                            <span className="text-xs text-slate-400">Total</span>
                        </div>
                    </div>

                    {/* Legend */}
                    <div className="grid grid-cols-2 gap-x-8 gap-y-3 w-full px-2">
                        {labels.map((label, index) => (
                            <div key={label} className="flex items-center gap-2">
                                <span
                                    className="w-2 h-2 rounded-full"
                                    style={{ backgroundColor: colors[index] }}
                                ></span>
                                <span className="text-xs text-slate-300 truncate">
                                    {label} ({Math.round(data[index] / total * 100)}%)
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default EquipmentChart;
