import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { datasetAPI } from '../services/api';
import UploadDropzone from '../components/UploadDropzone';
import StatsCards from '../components/StatsCards';
import EquipmentChart from '../components/EquipmentChart';
import EquipmentTable from '../components/EquipmentTable';
import DatasetList from '../components/DatasetList';

const Dashboard = () => {
    const { user, logout } = useAuth();
    const [datasets, setDatasets] = useState([]);
    const [selectedDataset, setSelectedDataset] = useState(null);
    const [stats, setStats] = useState(null);
    const [equipment, setEquipment] = useState([]);
    const [uploading, setUploading] = useState(false);
    const [loading, setLoading] = useState(true);

    const loadDatasets = useCallback(async () => {
        try {
            const response = await datasetAPI.list();
            setDatasets(response.data);
            if (response.data.length > 0 && !selectedDataset) {
                setSelectedDataset(response.data[0]);
            }
        } catch (err) {
            console.error('Failed to load datasets:', err);
        } finally {
            setLoading(false);
        }
    }, [selectedDataset]);

    const loadDatasetDetails = useCallback(async (dataset) => {
        if (!dataset) return;
        try {
            const [statsRes, equipmentRes] = await Promise.all([
                datasetAPI.getStats(dataset.id),
                datasetAPI.getEquipment(dataset.id),
            ]);
            setStats(statsRes.data);
            setEquipment(equipmentRes.data);
        } catch (err) {
            console.error('Failed to load dataset details:', err);
        }
    }, []);

    useEffect(() => {
        loadDatasets();
    }, [loadDatasets]);

    useEffect(() => {
        if (selectedDataset) {
            loadDatasetDetails(selectedDataset);
        }
    }, [selectedDataset, loadDatasetDetails]);

    const handleUpload = async (file) => {
        setUploading(true);
        try {
            await datasetAPI.upload(file);
            await loadDatasets();
        } catch (err) {
            console.error('Upload failed:', err);
        } finally {
            setUploading(false);
        }
    };

    const handleDownloadReport = async () => {
        if (!selectedDataset) return;
        try {
            const response = await datasetAPI.downloadReport(selectedDataset.id);
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${selectedDataset.name}_report.pdf`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (err) {
            console.error('Download failed:', err);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-background-dark flex items-center justify-center">
                <div className="spinner"></div>
            </div>
        );
    }

    return (
        <div className="bg-background-dark text-white font-display overflow-hidden antialiased h-screen w-screen flex relative">
            {/* Background Gradient */}
            <div className="absolute inset-0 bg-premium-gradient z-0 pointer-events-none"></div>

            {/* Sidebar */}
            <aside className="relative z-20 hidden w-72 flex-col border-r border-glass-border bg-[#0f172a]/80 backdrop-blur-xl lg:flex h-full">
                {/* Logo */}
                <div className="px-6 py-6">
                    <div className="flex flex-col">
                        <h1 className="text-2xl font-bold tracking-tight text-white drop-shadow-[0_0_10px_rgba(19,127,236,0.5)]">ChemVis</h1>
                        <p className="text-xs text-slate-400 font-medium tracking-wider uppercase opacity-80">Visualizer Pro</p>
                    </div>
                </div>

                {/* Upload Dropzone */}
                <div className="px-4 mb-6">
                    <UploadDropzone onUpload={handleUpload} uploading={uploading} />
                </div>

                {/* Navigation */}
                <nav className="flex-1 overflow-y-auto px-3 space-y-1">
                    <p className="px-3 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2 mt-4">Main Menu</p>
                    <a className="group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-white bg-primary/20 border border-primary/20 shadow-[0_0_10px_rgba(19,127,236,0.1)] transition-all" href="#">
                        <span className="material-symbols-outlined text-primary" style={{ fontVariationSettings: "'FILL' 1" }}>dashboard</span>
                        Dashboard
                    </a>

                    <p className="px-3 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2 mt-8">Recent Datasets</p>
                    <DatasetList
                        datasets={datasets}
                        selected={selectedDataset}
                        onSelect={setSelectedDataset}
                    />
                </nav>

                {/* User Profile */}
                <div className="border-t border-glass-border p-4">
                    <div className="flex items-center gap-3 rounded-lg bg-white/5 p-2 border border-white/5 hover:bg-white/10 transition-colors cursor-pointer">
                        <div className="relative h-10 w-10 overflow-hidden rounded-full bg-slate-700 flex items-center justify-center">
                            <span className="material-symbols-outlined text-slate-300">person</span>
                            <span className="absolute bottom-0 right-0 h-2.5 w-2.5 rounded-full border-2 border-[#0f172a] bg-green-500"></span>
                        </div>
                        <div className="flex-1 overflow-hidden">
                            <p className="truncate text-sm font-bold text-white">{user?.username || 'User'}</p>
                            <p className="truncate text-xs text-slate-400">Authenticated</p>
                        </div>
                        <button onClick={logout} className="text-slate-500 hover:text-red-400 transition-colors" title="Logout">
                            <span className="material-symbols-outlined text-lg">logout</span>
                        </button>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col relative z-10 overflow-hidden">
                {/* Header */}
                <header className="flex h-16 items-center justify-between border-b border-glass-border bg-[#0f172a]/60 backdrop-blur-md px-6 py-3">
                    <div className="flex items-center gap-2 text-sm text-slate-400">
                        <span className="hover:text-white cursor-pointer transition-colors">Home</span>
                        <span className="material-symbols-outlined text-[14px]">chevron_right</span>
                        <span className="text-white font-medium">Dashboard</span>
                    </div>

                    <div className="flex items-center gap-4">
                        {selectedDataset && (
                            <button
                                onClick={handleDownloadReport}
                                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-green-500/10 border border-green-500/20 text-green-400 text-sm font-medium hover:bg-green-500/20 transition-colors"
                            >
                                <span className="material-symbols-outlined text-lg">picture_as_pdf</span>
                                Download Report
                            </button>
                        )}
                    </div>
                </header>

                {/* Scrollable Content */}
                <div className="flex-1 overflow-y-auto p-6 scroll-smooth">
                    {selectedDataset ? (
                        <>
                            {/* Page Title */}
                            <div className="mb-6">
                                <h2 className="text-2xl font-bold text-white">{selectedDataset.name}</h2>
                                <p className="text-sm text-slate-400">Uploaded {new Date(selectedDataset.uploaded_at).toLocaleDateString()}</p>
                            </div>

                            {/* Stats Grid */}
                            <StatsCards stats={stats} />

                            {/* Charts Section */}
                            <EquipmentChart stats={stats} />

                            {/* Equipment Table */}
                            <div className="mt-6">
                                <EquipmentTable equipment={equipment} />
                            </div>
                        </>
                    ) : (
                        /* Empty State */
                        <div className="flex flex-col items-center justify-center h-full text-center">
                            <div className="w-24 h-24 rounded-full bg-primary/10 flex items-center justify-center mb-6">
                                <span className="material-symbols-outlined text-5xl text-primary/60">upload_file</span>
                            </div>
                            <h3 className="text-xl font-bold text-white mb-2">No Dataset Selected</h3>
                            <p className="text-slate-400 text-sm max-w-md">
                                Upload a CSV file to get started with your chemical equipment analysis.
                            </p>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
