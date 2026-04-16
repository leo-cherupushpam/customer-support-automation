"use client";

import { useState, useEffect, useCallback } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

// --- Types ---

interface TicketResult {
  ticket_id: string;
  category: string;
  confidence: number;
  auto_responded: boolean;
  response: string;
  quality_score?: number;
  priority?: string;
  escalation?: {
    context_summary?: string;
    suggested_response?: string;
  };
}

interface Analytics {
  total_tickets: number;
  deflection_rate: number;
  average_response_time: number;
  estimated_cost: number;
  category_distribution: Record<string, number>;
}

interface TicketSummary {
  ticket_id: string;
  category: string;
  auto_responded: boolean;
  confidence: number;
  response: string;
}

// --- Helper components ---

function Badge({
  children,
  color,
}: {
  children: React.ReactNode;
  color: "green" | "yellow" | "red" | "orange" | "blue" | "gray";
}) {
  const colorMap: Record<string, string> = {
    green: "bg-green-100 text-green-800",
    yellow: "bg-yellow-100 text-yellow-800",
    red: "bg-red-100 text-red-800",
    orange: "bg-orange-100 text-orange-800",
    blue: "bg-blue-100 text-blue-800",
    gray: "bg-gray-100 text-gray-700",
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colorMap[color]}`}
    >
      {children}
    </span>
  );
}

function priorityColor(priority?: string): "red" | "orange" | "yellow" | "green" | "gray" {
  switch (priority?.toLowerCase()) {
    case "urgent":
      return "red";
    case "high":
      return "orange";
    case "medium":
      return "yellow";
    case "low":
      return "green";
    default:
      return "gray";
  }
}

function MetricCard({
  label,
  value,
}: {
  label: string;
  value: string | number;
}) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4 text-center shadow-sm">
      <p className="text-sm text-gray-500 mb-1">{label}</p>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
    </div>
  );
}

// --- Main page ---

export default function Home() {
  const [ticketText, setTicketText] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<TicketResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [analyticsError, setAnalyticsError] = useState<string | null>(null);
  const [tickets, setTickets] = useState<TicketSummary[]>([]);
  const [ticketsError, setTicketsError] = useState<string | null>(null);
  const [ticketsLoading, setTicketsLoading] = useState(true);

  const fetchAnalytics = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/api/analytics`);
      if (!res.ok) throw new Error(`Analytics fetch failed: ${res.status}`);
      const data: Analytics = await res.json();
      setAnalytics(data);
      setAnalyticsError(null);
    } catch (err) {
      setAnalyticsError(err instanceof Error ? err.message : "Failed to load analytics");
    }
  }, []);

  const fetchTickets = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/api/tickets`);
      if (!res.ok) throw new Error(`Tickets fetch failed: ${res.status}`);
      const data: { tickets: TicketSummary[] } = await res.json();
      setTickets(data.tickets ?? []);
      setTicketsError(null);
    } catch (err) {
      setTicketsError(err instanceof Error ? err.message : "Failed to load tickets");
    } finally {
      setTicketsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAnalytics();
    fetchTickets();
  }, [fetchAnalytics, fetchTickets]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!ticketText.trim()) return;

    setSubmitting(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch(`${API_BASE}/api/tickets`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ticket_text: ticketText }),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData?.detail ?? `Request failed with status ${res.status}`);
      }

      const data: TicketResult = await res.json();
      setResult(data);
      setTicketText("");
      // Refresh analytics and tickets after submission
      await Promise.all([fetchAnalytics(), fetchTickets()]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An unexpected error occurred");
    } finally {
      setSubmitting(false);
    }
  }

  const recentTickets = [...tickets.slice(-5)].reverse();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">AI Customer Support Automation</h1>
          <p className="mt-1 text-sm text-gray-500">
            Intelligent ticket routing and automated response generation
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Two-column layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left: Ticket submission + result */}
          <div className="space-y-6">
            {/* Submission form */}
            <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Submit a Support Ticket</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <textarea
                  value={ticketText}
                  onChange={(e) => setTicketText(e.target.value)}
                  placeholder="Describe your issue..."
                  rows={6}
                  disabled={submitting}
                  className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none disabled:bg-gray-50 disabled:text-gray-400"
                />
                {error && (
                  <div className="rounded-md bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
                    {error}
                  </div>
                )}
                <button
                  type="submit"
                  disabled={submitting || !ticketText.trim()}
                  className="w-full rounded-md bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {submitting ? "Processing..." : "Process Ticket"}
                </button>
              </form>
            </div>

            {/* Result panel */}
            {result && (
              <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-6 space-y-4">
                <div className="flex items-center gap-3">
                  {result.auto_responded ? (
                    <Badge color="green">Auto-Responded</Badge>
                  ) : (
                    <Badge color="yellow">Escalated to Human</Badge>
                  )}
                  <span className="text-sm text-gray-500 font-mono truncate max-w-[180px]" title={result.ticket_id}>
                    #{result.ticket_id}
                  </span>
                </div>

                <div className="flex flex-wrap gap-3 text-sm">
                  <span className="text-gray-600">
                    <span className="font-medium text-gray-800">Category:</span> {result.category}
                  </span>
                  <span className="text-gray-600">
                    <span className="font-medium text-gray-800">Confidence:</span>{" "}
                    {(result.confidence * 100).toFixed(0)}%
                  </span>
                  {result.quality_score !== undefined && (
                    <span className="text-gray-600">
                      <span className="font-medium text-gray-800">Quality:</span>{" "}
                      {(result.quality_score * 100).toFixed(0)}%
                    </span>
                  )}
                  {!result.auto_responded && result.priority && (
                    <Badge color={priorityColor(result.priority)}>
                      {result.priority.charAt(0).toUpperCase() + result.priority.slice(1)} Priority
                    </Badge>
                  )}
                </div>

                {result.auto_responded ? (
                  <div className="rounded-md bg-green-50 border border-green-200 p-4">
                    <p className="text-sm font-medium text-green-800 mb-2">AI Response</p>
                    <p className="text-sm text-green-900 whitespace-pre-wrap">{result.response}</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {result.escalation?.context_summary && (
                      <div className="rounded-md bg-yellow-50 border border-yellow-200 p-4">
                        <p className="text-sm font-medium text-yellow-800 mb-1">Context Summary</p>
                        <p className="text-sm text-yellow-900">{result.escalation.context_summary}</p>
                      </div>
                    )}
                    {(result.escalation?.suggested_response || result.response) && (
                      <div className="rounded-md bg-blue-50 border border-blue-200 p-4">
                        <p className="text-sm font-medium text-blue-800 mb-2">Suggested Response</p>
                        <p className="text-sm text-blue-900 whitespace-pre-wrap">
                          {result.escalation?.suggested_response ?? result.response}
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Right: Analytics */}
          <div className="space-y-6">
            <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Analytics Dashboard</h2>

              {analyticsError ? (
                <div className="rounded-md bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
                  {analyticsError}
                </div>
              ) : analytics ? (
                <div className="space-y-6">
                  <div className="grid grid-cols-2 gap-3">
                    <MetricCard
                      label="Total Tickets"
                      value={analytics.total_tickets}
                    />
                    <MetricCard
                      label="Deflection Rate"
                      value={`${(analytics.deflection_rate * 100).toFixed(1)}%`}
                    />
                    <MetricCard
                      label="Avg Response Time"
                      value={`${analytics.average_response_time.toFixed(2)}s`}
                    />
                    <MetricCard
                      label="Est. Cost"
                      value={`$${analytics.estimated_cost.toFixed(4)}`}
                    />
                  </div>

                  {analytics.category_distribution &&
                    Object.keys(analytics.category_distribution).length > 0 && (
                      <div>
                        <h3 className="text-sm font-medium text-gray-700 mb-3">
                          Category Distribution
                        </h3>
                        <ul className="space-y-2">
                          {Object.entries(analytics.category_distribution)
                            .sort(([, a], [, b]) => b - a)
                            .map(([category, count]) => (
                              <li
                                key={category}
                                className="flex items-center justify-between text-sm"
                              >
                                <span className="text-gray-700 capitalize">{category}</span>
                                <span className="font-medium text-gray-900 bg-gray-100 px-2 py-0.5 rounded">
                                  {count}
                                </span>
                              </li>
                            ))}
                        </ul>
                      </div>
                    )}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-400 text-sm">Loading analytics...</div>
              )}
            </div>
          </div>
        </div>

        {/* Ticket history */}
        <div className="mt-8">
          <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Tickets</h2>

            {ticketsError ? (
              <div className="rounded-md bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
                {ticketsError}
              </div>
            ) : ticketsLoading ? (
              <p className="text-sm text-gray-400 text-center py-6">Loading tickets...</p>
            ) : recentTickets.length === 0 ? (
              <p className="text-sm text-gray-400 text-center py-6">No tickets yet.</p>
            ) : (
              <div className="space-y-3">
                {recentTickets.map((ticket) => (
                  <div
                    key={ticket.ticket_id}
                    className="flex items-start gap-4 rounded-md border border-gray-100 bg-gray-50 px-4 py-3"
                  >
                    <div className="min-w-0 flex-1">
                      <div className="flex flex-wrap items-center gap-2 mb-1">
                        <span
                          className="text-xs font-mono text-gray-400 truncate max-w-[140px]"
                          title={ticket.ticket_id}
                        >
                          #{ticket.ticket_id.length > 12 ? `${ticket.ticket_id.slice(0, 12)}...` : ticket.ticket_id}
                        </span>
                        <span className="text-xs text-gray-600 capitalize font-medium">
                          {ticket.category}
                        </span>
                        {ticket.auto_responded ? (
                          <Badge color="green">Auto</Badge>
                        ) : (
                          <Badge color="yellow">Escalated</Badge>
                        )}
                        <span className="text-xs text-gray-400">
                          {(ticket.confidence * 100).toFixed(0)}% confidence
                        </span>
                      </div>
                      {ticket.response && (
                        <p className="text-sm text-gray-600 line-clamp-2">
                          {ticket.response.slice(0, 120)}
                          {ticket.response.length > 120 ? "..." : ""}
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
