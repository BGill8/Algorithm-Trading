"use client";

import { useState } from 'react';
import { Container, TextField, Button, Typography, Paper, CircularProgress, Box, Alert } from '@mui/material';

// Define types for our state
interface FinancialData {
    years: string[];
    revenues: number[];
    revenue_growths: number[];
}

interface Projections {
    base_case: number;
    bull_case: number;
    bear_case: number;
}

export default function Home() {
    const [ticker, setTicker] = useState('');
    const [financials, setFinancials] = useState<FinancialData | null>(null);
    const [projections, setProjections] = useState<Projections | null>(null);
    const [forecastYears, setForecastYears] = useState(5);
    const [forecast, setForecast] = useState({
        base: Array(forecastYears).fill(0.10),
        bull: Array(forecastYears).fill(0.15),
        bear: Array(forecastYears).fill(0.05),
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleFetchFinancials = async () => {
        if (!ticker) {
            setError("Please enter a ticker symbol.");
            return;
        }
        setLoading(true);
        setError(null);
        setFinancials(null);
        setProjections(null);

        try {
            const res = await fetch(`http://127.0.0.1:8000/api/stock/${ticker}`);
            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || "Failed to fetch financial data.");
            }
            const data: FinancialData = await res.json();
            setFinancials(data);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleCalculateProjections = async () => {
        if (!ticker) {
            setError("Please fetch financial data for a ticker first.");
            return;
        }
        setLoading(true);
        setError(null);

        try {
            const res = await fetch('http://127.0.0.1:8000/api/calculate_projection', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    ticker: ticker,
                    revenue_growth_forecast: forecast,
                }),
            });
            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || "Failed to calculate projections.");
            }
            const data: Projections = await res.json();
            setProjections(data);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };
    
    const handleForecastChange = (caseName: 'base' | 'bull' | 'bear', index: number, value: string) => {
        const newForecast = { ...forecast };
        newForecast[caseName][index] = parseFloat(value) / 100;
        setForecast(newForecast);
    };


    return (
        <Container maxWidth="md" sx={{ mt: 4 }}>
            <Paper sx={{ p: 3 }}>
                <Typography variant="h4" component="h1" gutterBottom>
                    Stock Projection Calculator
                </Typography>
                
                {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

                <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
                    <TextField
                        label="Stock Ticker"
                        variant="outlined"
                        value={ticker}
                        onChange={(e) => setTicker(e.target.value.toUpperCase())}
                        fullWidth
                    />
                    <Button variant="contained" onClick={handleFetchFinancials} disabled={loading}>
                        {loading ? <CircularProgress size={24} /> : 'Get Data'}
                    </Button>
                </Box>

                {financials && (
                    <Box>
                        <Typography variant="h5" gutterBottom>{ticker} Historical Revenue</Typography>
                        {financials.years.map((year, i) => (
                            <Typography key={year}>
                                {year}: ${ (financials.revenues[i] / 1e9).toFixed(2) }B 
                                (Growth: { (financials.revenue_growths[i] * 100).toFixed(2) }%)
                            </Typography>
                        ))}
                        
                        <Typography variant="h5" sx={{ mt: 3, mb: 1 }}>Revenue Growth Forecast (%)</Typography>
                        
                        {['base', 'bull', 'bear'].map((caseName) => (
                             <Box key={caseName} sx={{ display: 'flex', gap: 1, alignItems: 'center', mb: 1 }}>
                                <Typography sx={{ width: '60px' }}>{caseName.charAt(0).toUpperCase() + caseName.slice(1)}:</Typography>
                                {forecast[caseName as 'base' | 'bull' | 'bear'].map((val, i) => (
                                    <TextField
                                        key={i}
                                        type="number"
                                        size="small"
                                        defaultValue={val * 100}
                                        onChange={(e) => handleForecastChange(caseName as 'base' | 'bull' | 'bear', i, e.target.value)}
                                        sx={{ width: '80px' }}
                                    />
                                ))}
                            </Box>
                        ))}
                        
                        <Button variant="contained" color="secondary" onClick={handleCalculateProjections} disabled={loading} sx={{ mt: 2 }}>
                            {loading ? <CircularProgress size={24} /> : 'Calculate Projection'}
                        </Button>
                    </Box>
                )}

                {projections && (
                    <Box sx={{ mt: 3 }}>
                        <Typography variant="h5" gutterBottom>Projected Stock Price ({forecastYears} Years)</Typography>
                        <Typography><b>Bull Case:</b> ${projections.bull_case.toFixed(2)}</Typography>
                        <Typography><b>Base Case:</b> ${projections.base_case.toFixed(2)}</Typography>
                        <Typography><b>Bear Case:</b> ${projections.bear_case.toFixed(2)}</Typography>
                    </Box>
                )}
            </Paper>
        </Container>
    );
}
