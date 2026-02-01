import React, { useState } from 'react';
import { submitPredictionRequest, checkRequestStatus, submitFeedback } from './api';

const HousingForm = () => {
    const [formData, setFormData] = useState({
        area: 100, // Default now in m2 (approx 1000 sqft)
        bedrooms: 3,
        bathrooms: 1,
        stories: 1,
        mainroad: true,
        guestroom: false,
        basement: false,
        hotwaterheating: false,
        airconditioning: false,
        parking: 1,
        prefarea: false,
        furnishingstatus: 'furnished'
    });

    const [status, setStatus] = useState('IDLE');
    const [result, setResult] = useState(null);
    const [showFeedback, setShowFeedback] = useState(false);
    const [soldPrice, setSoldPrice] = useState('');

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus('SUBMITTING');
        try {
            // CONVERSION LOGIC: m2 -> sqft
            // 1 m2 = 10.7639 sqft
            const payload = {
                ...formData,
                area: Math.round(Number(formData.area) * 10.7639),
                bedrooms: Number(formData.bedrooms),
                bathrooms: Number(formData.bathrooms),
                stories: Number(formData.stories),
                parking: Number(formData.parking)
            };

            const resp = await submitPredictionRequest(payload);
            setStatus('QUEUED');
            pollStatus(resp.data.request_id);
        } catch (err) {
            console.error(err);
            setStatus('ERROR');
        }
    };

    const pollStatus = async (id) => {
        const interval = setInterval(async () => {
            try {
                const resp = await checkRequestStatus(id);
                if (resp.data.status === 'COMPLETED') {
                    clearInterval(interval);
                    setResult(resp.data.result);
                    setStatus('COMPLETED');
                } else {
                    setStatus(resp.data.status);
                }
            } catch (err) {
                clearInterval(interval);
                setStatus('ERROR');
            }
        }, 1000);
    };

    const [notification, setNotification] = useState(null);

    const handleFeedbackSubmit = async () => {
        if (!result || !soldPrice) return;
        try {
            await submitFeedback({
                request_id: result.request_id,
                actual_price: parseFloat(soldPrice)
            });
            // Show custom notification
            setNotification({
                title: "Hvala na informaciji! 🧠",
                message: "Agent je naučio novu informaciju! Trening je automatski pokrenut.",
                type: "success"
            });
            setShowFeedback(false);
            setSoldPrice('');
        } catch (e) {
            setNotification({
                title: "Greška ⚠️",
                message: "Došlo je do problema pri slanju podataka.",
                type: "error"
            });
        }
    };

    const closeNotification = () => setNotification(null);

    const translateConfidence = (conf) => {
        switch (conf) {
            case 'HIGH': return 'VISOKA';
            case 'MEDIUM': return 'SREDNJA';
            case 'LOW': return 'NISKA';
            default: return conf;
        }
    };

    const translateStatus = (s) => {
        switch (s) {
            case 'IDLE': return 'Spreman';
            case 'SUBMITTING': return 'Šaljem...';
            case 'QUEUED': return 'U redu čekanja...';
            case 'PROCESSING': return 'Agent Razmišlja...';
            case 'COMPLETED': return 'Završeno';
            case 'ERROR': return 'Greška';
            default: return s;
        }
    };

    return (
        <>
            {notification && (
                <div className="fixed inset-0 flex items-center justify-center z-50 bg-black/40 backdrop-blur-sm animate-fade-in">
                    <div className="bg-white p-6 rounded-2xl shadow-2xl max-w-sm w-full mx-4 border border-stone-100 transform transition-all scale-100">
                        <div className={`text-xl font-bold mb-2 ${notification.type === 'error' ? 'text-red-800' : 'text-stone-800'}`}>
                            {notification.title}
                        </div>
                        <p className="text-stone-500 mb-6 leading-relaxed">
                            {notification.message}
                        </p>
                        <button
                            onClick={closeNotification}
                            className="w-full py-2 bg-stone-800 text-white rounded-lg hover:bg-stone-900 transition-colors font-medium"
                        >
                            Uredu
                        </button>
                    </div>
                </div>
            )}

            <div className="max-w-3xl mx-auto p-8 mt-10 bg-white/80 backdrop-blur-xl rounded-2xl shadow-xl border border-white/50">
                <div className="text-center mb-10 pb-4">
                    <h2 className="text-4xl font-bold text-stone-800 tracking-tight">
                        Agent za Nekretnine
                    </h2>
                    <p className="text-stone-500 mt-2 font-medium">Ekskluzivna AI Procjena Vrijednosti</p>
                </div>

                {status === 'COMPLETED' && result ? (
                    <div className="bg-gradient-to-br from-stone-50 to-white rounded-xl p-8 border border-stone-200 shadow-sm text-center animate-fade-in transition-all">
                        <h3 className="text-xs font-bold text-stone-500 uppercase tracking-widest mb-2">Procijenjena Vrijednost</h3>
                        <p className="text-5xl font-extrabold text-stone-800 drop-shadow-sm">
                            KM {result.estimated_price.toLocaleString()}
                        </p>

                        <div className="mt-6 flex justify-center gap-4">
                            <div className={`px-4 py-1.5 rounded-full text-xs font-bold border ${getResultColor(result.confidence)}`}>
                                Pouzdanost: {translateConfidence(result.confidence)}
                            </div>
                        </div>

                        {result.rule_generated_warnings?.length > 0 && (
                            <div className="mt-6 p-4 bg-orange-50/50 text-stone-700 text-sm rounded-xl text-left border border-orange-100">
                                <strong className="text-orange-800">⚠️ Napomena:</strong>
                                <ul className="list-disc pl-5 mt-2 space-y-1 text-stone-600">
                                    {result.rule_generated_warnings.map((w, i) => <li key={i}>{w}</li>)}
                                </ul>
                            </div>
                        )}

                        <div className="mt-8 flex justify-center gap-4">
                            <button
                                onClick={() => { setStatus('IDLE'); setResult(null); setShowFeedback(false); }}
                                className="px-6 py-2.5 bg-white text-stone-800 border border-stone-200 rounded-xl hover:bg-stone-50 transition-all shadow-sm font-semibold tracking-wide"
                            >
                                Nova Procjena
                            </button>
                            <button
                                onClick={() => setShowFeedback(true)}
                                className="px-6 py-2.5 bg-stone-800 text-white rounded-xl hover:bg-stone-900 transition-all shadow-lg hover:shadow-xl font-semibold transform hover:-translate-y-0.5"
                            >
                                Tačna Cijena? (Nauči Agenta)
                            </button>
                        </div>

                        {showFeedback && (
                            <div className="mt-6 p-6 bg-white rounded-xl border border-stone-100 shadow-sm text-left">
                                <label className="block text-sm font-semibold text-stone-700 mb-2">
                                    Koja je bila stvarna prodajna cijena? (KM)
                                </label>
                                <div className="flex gap-3">
                                    <input
                                        type="number"
                                        className="flex-1 rounded-lg border-stone-200 bg-stone-50/50 p-3 shadow-inner focus:bg-white focus:border-stone-400 focus:ring-2 focus:ring-stone-100 transition-all outline-none"
                                        placeholder="npr. 350000"
                                        value={soldPrice}
                                        onChange={(e) => setSoldPrice(e.target.value)}
                                    />
                                    <button
                                        onClick={handleFeedbackSubmit}
                                        className="bg-stone-800 text-white px-6 py-2 rounded-lg hover:bg-stone-900 shadow-md font-medium"
                                    >
                                        Pošalji
                                    </button>
                                </div>
                                <p className="text-xs text-stone-400 mt-3 font-medium">
                                    * Ovi podaci se koriste za 'Continuous Learning' agenta.
                                </p>
                            </div>
                        )}
                    </div>
                ) : (
                    <form onSubmit={handleSubmit} className="space-y-6 text-stone-700">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <InputField label="Površina (m²)" name="area" type="number" value={formData.area} onChange={handleChange} />
                            <SelectField label="Namještenost" name="furnishingstatus" value={formData.furnishingstatus} onChange={handleChange}>
                                <option value="furnished">Potpuno namješteno</option>
                                <option value="semi-furnished">Polu-namješteno</option>
                                <option value="unfurnished">Nenamješteno</option>
                            </SelectField>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                            <InputField label="Broj Soba" name="bedrooms" type="number" value={formData.bedrooms} onChange={handleChange} />
                            <InputField label="Broj Kupatila" name="bathrooms" type="number" value={formData.bathrooms} onChange={handleChange} />
                            <InputField label="Broj Spratova" name="stories" type="number" value={formData.stories} onChange={handleChange} />
                            <InputField label="Parking Mjesta" name="parking" type="number" value={formData.parking} onChange={handleChange} />
                        </div>

                        <div className="p-6 bg-stone-50/50 rounded-2xl border border-stone-100 grid grid-cols-2 md:grid-cols-3 gap-y-5 shadow-inner">
                            <CheckboxField label="Glavna Cesta" name="mainroad" checked={formData.mainroad} onChange={handleChange} />
                            <CheckboxField label="Gostinjska Soba" name="guestroom" checked={formData.guestroom} onChange={handleChange} />
                            <CheckboxField label="Podrum" name="basement" checked={formData.basement} onChange={handleChange} />
                            <CheckboxField label="Grijanje Vode" name="hotwaterheating" checked={formData.hotwaterheating} onChange={handleChange} />
                            <CheckboxField label="Klima Uređaj" name="airconditioning" checked={formData.airconditioning} onChange={handleChange} />
                            <CheckboxField label="Atraktivna Lokacija" name="prefarea" checked={formData.prefarea} onChange={handleChange} />
                        </div>

                        <button
                            type="submit"
                            disabled={status !== 'IDLE'}
                            className={`w-full py-4 px-6 rounded-xl shadow-lg text-lg font-bold text-white transition-all transform hover:-translate-y-0.5
                        ${status !== 'IDLE'
                                    ? 'bg-stone-400 cursor-not-allowed animate-pulse'
                                    : 'bg-stone-800 hover:bg-stone-900 shadow-stone-800/20'}`}
                        >
                            {status === 'IDLE' ? 'Procijeni Vrijednost' : `${translateStatus(status)}`}
                        </button>
                    </form>
                )}
            </div>
        </>
    );
};

// UI Components
const InputField = ({ label, ...props }) => (
    <div>
        <label className="block text-sm font-semibold text-stone-600 mb-1.5 uppercase tracking-wider">{label}</label>
        <input
            className="w-full rounded-lg border-stone-200 bg-white p-3 text-stone-800 focus:bg-amber-50 focus:border-amber-600 focus:ring-2 focus:ring-amber-200 transition-all outline-none border shadow-sm"
            {...props}
        />
    </div>
);

const SelectField = ({ label, children, ...props }) => (
    <div>
        <label className="block text-sm font-semibold text-stone-600 mb-1.5 uppercase tracking-wider">{label}</label>
        <select
            className="w-full rounded-lg border-stone-200 bg-white p-3 text-stone-800 focus:bg-amber-50 focus:border-amber-600 focus:ring-2 focus:ring-amber-200 transition-all outline-none border shadow-sm"
            {...props}
        >
            {children}
        </select>
    </div >
);

const CheckboxField = ({ label, ...props }) => (
    <label className="flex items-center space-x-3 cursor-pointer group">
        <input
            type="checkbox"
            className="w-5 h-5 rounded border-stone-300 text-amber-800 focus:ring-amber-600 transition-colors bg-white checked:bg-amber-800"
            {...props}
        />
        <span className="text-sm font-medium text-stone-600 group-hover:text-amber-800 transition-colors">{label}</span>
    </label>
);

const getResultColor = (conf) => {
    switch (conf) {
        case 'HIGH': return 'bg-emerald-100 text-emerald-900 border-emerald-300';
        case 'MEDIUM': return 'bg-amber-100 text-amber-900 border-amber-300';
        case 'LOW': return 'bg-red-100 text-red-900 border-red-300';
        default: return 'bg-stone-100';
    }
}

export default HousingForm;
