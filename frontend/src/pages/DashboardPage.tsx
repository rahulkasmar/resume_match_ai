import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import api from '../lib/api';
import { Loader2, BotMessageSquare, Copy, LogOut, Check, Sparkles, FileText, Briefcase } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import Header from '../components/ui/Header';
import Footer from '../components/ui/Footer';

// --- Reusable UI Components ---
const ResultCard = ({ title, items, icon: Icon }: { title: string; items: string[]; icon: React.ElementType }) => (
    <div className="bg-white/80 backdrop-blur-sm p-6 rounded-xl shadow-lg border border-gray-200">
      <div className="flex items-center mb-4"><Icon className="h-6 w-6 text-primary" /><h3 className="text-lg font-semibold text-gray-900 ml-3">{title}</h3></div>
      <ul className="space-y-2">{items.map((item, index) => (<li key={index} className="flex items-start text-gray-600"><span className="text-primary font-bold mr-3 mt-1">▪</span><span>{item}</span></li>))}</ul>
    </div>
);

const SkeletonLoader = () => (
    <div className="space-y-8 animate-pulse">
        <div className="bg-white/50 h-24 rounded-xl"></div>
        <div className="grid md:grid-cols-2 gap-8"><div className="bg-white/50 h-48 rounded-xl"></div><div className="bg-white/50 h-48 rounded-xl"></div></div>
    </div>
);

// --- ADD THIS COMPONENT ---
const CoverLetterDisplay = ({ text }: { text: string }) => {
    const [copied, setCopied] = useState(false);
    const handleCopy = () => {
      navigator.clipboard.writeText(text);
      setCopied(true);
      toast.success('Copied to clipboard!');
      setTimeout(() => setCopied(false), 2000);
    };
  
    return (
      <div className="bg-white/80 backdrop-blur-sm p-6 rounded-xl shadow-lg border border-gray-200">
        <div className="flex justify-between items-center mb-4">
          <div className="flex items-center">
            <BotMessageSquare className="h-6 w-6 text-primary" />
            <h3 className="text-lg font-semibold text-gray-900 ml-3">Generated Cover Letter</h3>
          </div>
          <button onClick={handleCopy} className="p-2 rounded-lg hover:bg-gray-100 text-gray-500 transition-colors" title="Copy to Clipboard">
            {copied ? <Check size={18} className="text-green-500" /> : <Copy size={18} />}
          </button>
        </div>
        <pre className="text-gray-700 text-sm whitespace-pre-wrap font-sans bg-gray-50 p-4 rounded-md border">{text}</pre>
      </div>
    );
};

// --- Main Page Component ---
const analyzeResume = async (formData: FormData) => {
  const { data } = await api.post('/analysis/', formData);
  return data;
};

export default function DashboardPage() {
  const [jobDescription, setJobDescription] = useState('');
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  
  const mutation = useMutation({
    mutationFn: analyzeResume,
    onSuccess: () => toast.success('Analysis complete!'),
    onError: () => toast.error('Analysis failed. Please check your file and try again.'),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!resumeFile || !jobDescription.trim()) return toast.error('Please provide a resume and job description.');
    const formData = new FormData();
    formData.append('resume_file', resumeFile);
    formData.append('job_description', jobDescription);
    mutation.mutate(formData);
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-grow max-w-6xl mx-auto py-12 px-4 w-full">
        <div className="text-center mb-12">
            <h2 className="text-4xl font-extrabold text-gray-900">Get Your Instant Analysis</h2>
            <p className="mt-3 text-lg text-gray-600">Upload your resume and a job description to see how you match up.</p>
        </div>
        
        <div className="bg-white/60 backdrop-blur-sm p-8 rounded-xl shadow-2xl border border-gray-200 mb-12">
            {/* The form code is unchanged */}
            <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
            <div className="space-y-2">
              <label className="flex items-center text-lg font-semibold text-gray-700"><Briefcase className="mr-2 h-5 w-5"/> Job Description</label>
              <textarea className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary transition h-64" value={jobDescription} onChange={(e) => setJobDescription(e.target.value)} placeholder="Paste the full job description here..."/>
            </div>
            <div className="space-y-6">
                <div className="space-y-2">
                    <label className="flex items-center text-lg font-semibold text-gray-700"><FileText className="mr-2 h-5 w-5"/> Your Resume</label>
                    <input type="file" accept=".pdf,.docx" className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary hover:file:bg-primary-100 cursor-pointer" onChange={(e) => setResumeFile(e.target.files ? e.target.files[0] : null)}/>
                </div>
                <button type="submit" className="w-full px-6 py-4 bg-primary text-white font-bold rounded-lg hover:bg-primary-700 disabled:bg-gray-400 flex items-center justify-center transition-colors text-lg shadow-lg hover:shadow-xl" disabled={mutation.isPending}>
                    {mutation.isPending ? <Loader2 className="mr-2 h-6 w-6 animate-spin" /> : <BotMessageSquare className="mr-2 h-6 w-6" />}
                    {mutation.isPending ? 'Analyzing...' : 'Analyze Now'}
                </button>
            </div>
          </form>
        </div>

        {/* Results Section */}
        {mutation.isPending && <SkeletonLoader />}
        {mutation.data && (
          <div className="space-y-8">
             <div className="bg-white/60 backdrop-blur-sm border border-gray-200 p-8 rounded-xl shadow-lg text-center"><h3 className="text-xl font-semibold text-gray-800 mb-3">Match Score</h3><p className="text-6xl font-bold text-primary">{mutation.data.match_score.toFixed(2)}%</p></div>
             <div className="grid md:grid-cols-2 gap-8"><ResultCard title="Missing Skills" items={mutation.data.missing_skills} icon={Briefcase} /><ResultCard title="Resume Suggestions" items={mutation.data.resume_suggestions} icon={FileText}/></div>
             {/* --- ADD THIS LINE --- */}
             <CoverLetterDisplay text={mutation.data.generated_cover_letter} />
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}