import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

const UploadDropzone = ({ onUpload, uploading }) => {
    const onDrop = useCallback((acceptedFiles) => {
        if (acceptedFiles.length > 0) {
            onUpload(acceptedFiles[0]);
        }
    }, [onUpload]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
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
        ${isDragActive
                    ? 'border-primary bg-primary/20 shadow-[0_0_20px_rgba(19,127,236,0.3)]'
                    : 'border-primary/50 bg-primary/5 hover:border-primary hover:bg-primary/10 hover:shadow-[0_0_15px_rgba(19,127,236,0.15)]'
                }
        ${uploading ? 'opacity-50 cursor-not-allowed' : ''}
      `}
        >
            <input {...getInputProps()} />

            {uploading ? (
                <div className="w-8 h-8 border-2 border-primary/30 border-t-primary rounded-full animate-spin"></div>
            ) : (
                <span className="material-symbols-outlined text-primary text-3xl transition-transform group-hover:scale-110">
                    cloud_upload
                </span>
            )}

            <div className="text-center">
                <p className="text-sm font-bold text-white">
                    {uploading ? 'Uploading...' : 'Upload Dropzone'}
                </p>
                <p className="text-[10px] text-slate-400 mt-1">
                    {isDragActive ? 'Drop the file here' : 'Drag CSV files here'}
                </p>
            </div>
        </div>
    );
};

export default UploadDropzone;
