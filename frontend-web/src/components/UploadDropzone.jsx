import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';

const UploadDropzone = ({ onUpload, uploading, onError }) => {
    const [error, setError] = useState(null);

    const onDrop = useCallback((acceptedFiles) => {
        setError(null);
        if (acceptedFiles.length > 0) {
            onUpload(acceptedFiles[0]);
        }
    }, [onUpload]);

    const onDropRejected = useCallback((rejectedFiles) => {
        if (rejectedFiles.length > 0) {
            const { errors } = rejectedFiles[0];
            let errorMessage = 'Invalid file';
            if (errors[0]?.code === 'file-invalid-type') {
                errorMessage = 'Only CSV files are allowed';
            }
            setError(errorMessage);
            onError?.(errorMessage);
            // Clear error after 4 seconds
            setTimeout(() => setError(null), 4000);
        }
    }, [onError]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        onDropRejected,
        accept: { 'text/csv': ['.csv'] },
        multiple: false,
        disabled: uploading,
    });

    return (
        <div
            {...getRootProps()}
            className={`
        relative group cursor-pointer flex flex-col items-center justify-center gap-3 
        rounded-xl border border-dashed px-4 py-8 transition-all
        ${error
                    ? 'border-red-500 bg-red-500/10 shadow-[0_0_15px_rgba(239,68,68,0.2)]'
                    : isDragActive
                        ? 'border-primary bg-primary/20 shadow-[0_0_20px_rgba(19,127,236,0.3)]'
                        : 'border-primary/50 bg-primary/5 hover:border-primary hover:bg-primary/10 hover:shadow-[0_0_15px_rgba(19,127,236,0.15)]'
                }
        ${uploading ? 'opacity-50 cursor-not-allowed' : ''}
      `}
        >
            <input {...getInputProps()} />

            {uploading ? (
                <div className="w-8 h-8 border-2 border-primary/30 border-t-primary rounded-full animate-spin"></div>
            ) : error ? (
                <span className="material-symbols-outlined text-red-400 text-3xl">
                    error
                </span>
            ) : (
                <span className="material-symbols-outlined text-primary text-3xl transition-transform group-hover:scale-110">
                    cloud_upload
                </span>
            )}

            <div className="text-center">
                <p className={`text-sm font-bold ${error ? 'text-red-400' : 'text-white'}`}>
                    {uploading ? 'Uploading...' : error ? error : 'Upload Dropzone'}
                </p>
                <p className="text-[10px] text-slate-400 mt-1">
                    {error ? 'Please select a valid CSV file' : isDragActive ? 'Drop the file here' : 'Drag CSV files here'}
                </p>
            </div>
        </div>
    );
};

export default UploadDropzone;
