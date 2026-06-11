import * as vscode from 'vscode';

export interface PhaseRequest {
  project_name: string;
  context?: string;
}

export class BackendClient {
  get baseUrl(): string {
    return vscode.workspace
      .getConfiguration('adcp')
      .get<string>('backendUrl', 'http://localhost:8000');
  }

  async runPhase(endpoint: string, payload: PhaseRequest): Promise<string> {
    const url = `${this.baseUrl}/${endpoint}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP ${response.status}: ${errorText}`);
    }

    const data = (await response.json()) as { result: string };
    return data.result;
  }

  async checkHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      return response.ok;
    } catch {
      return false;
    }
  }
}
