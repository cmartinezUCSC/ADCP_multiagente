import * as vscode from 'vscode';
import { StateManager, AdcpPhase } from './stateManager';

export class AdcpPanel {
  public static currentPanel: AdcpPanel | undefined;
  private static readonly viewType = 'adcpPanel';

  private readonly _panel: vscode.WebviewPanel;
  private _disposables: vscode.Disposable[] = [];

  public static createOrShow(
    _extensionUri: vscode.Uri,
    stateManager: StateManager
  ): void {
    const column = vscode.window.activeTextEditor
      ? vscode.ViewColumn.Beside
      : vscode.ViewColumn.One;

    if (AdcpPanel.currentPanel) {
      AdcpPanel.currentPanel._panel.reveal(column);
      AdcpPanel.currentPanel._update(stateManager);
      return;
    }

    const panel = vscode.window.createWebviewPanel(
      AdcpPanel.viewType,
      'ADCP Multiagente',
      column,
      {
        enableScripts: true,
        retainContextWhenHidden: true,
      }
    );

    AdcpPanel.currentPanel = new AdcpPanel(panel, stateManager);
  }

  private constructor(
    panel: vscode.WebviewPanel,
    stateManager: StateManager
  ) {
    this._panel = panel;
    this._update(stateManager);

    this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
  }

  public dispose(): void {
    AdcpPanel.currentPanel = undefined;
    this._panel.dispose();
    while (this._disposables.length) {
      const disposable = this._disposables.pop();
      if (disposable) {
        disposable.dispose();
      }
    }
  }

  private _update(stateManager: StateManager): void {
    this._panel.webview.html = this._getHtmlContent(stateManager);
  }

  private _getHtmlContent(stateManager: StateManager): string {
    const projectName = stateManager.getProjectName() ?? '(sin proyecto)';
    const phases = Object.values(AdcpPhase);

    const phaseSections = phases
      .map((phase) => {
        const result = stateManager.getPhaseResult(phase);
        const isComplete = result !== undefined;
        const statusIcon = isComplete ? '✅' : '⏳';
        const resultHtml = isComplete
          ? `<div class="result">${escapeHtml(result ?? '')}</div>`
          : `<p class="pending">Pendiente — ejecuta el comando "ADCP: ${phase}"</p>`;

        return `
        <section class="phase ${isComplete ? 'complete' : 'pending'}">
          <h2>${statusIcon} ${escapeHtml(phase)}</h2>
          ${resultHtml}
        </section>`;
      })
      .join('\n');

    return `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline';" />
  <title>ADCP Multiagente</title>
  <style>
    body {
      font-family: var(--vscode-font-family, sans-serif);
      font-size: var(--vscode-font-size, 13px);
      color: var(--vscode-editor-foreground);
      background: var(--vscode-editor-background);
      padding: 16px;
      line-height: 1.6;
    }
    h1 { color: var(--vscode-titleBar-activeForeground); border-bottom: 1px solid var(--vscode-panel-border); padding-bottom: 8px; }
    h2 { font-size: 1em; margin-bottom: 4px; }
    .phase { border: 1px solid var(--vscode-panel-border); border-radius: 4px; padding: 12px; margin-bottom: 12px; }
    .phase.complete { border-color: var(--vscode-testing-iconPassed, #73c991); }
    .phase.pending { opacity: 0.7; }
    .result { white-space: pre-wrap; word-break: break-word; background: var(--vscode-textBlockQuote-background); padding: 8px; border-radius: 3px; max-height: 300px; overflow-y: auto; }
    .pending { font-style: italic; color: var(--vscode-descriptionForeground); }
    .project-label { font-size: 0.9em; color: var(--vscode-descriptionForeground); margin-bottom: 16px; }
  </style>
</head>
<body>
  <h1>🤖 ADCP Multiagente</h1>
  <p class="project-label">Proyecto: <strong>${escapeHtml(projectName)}</strong></p>
  ${phaseSections}
</body>
</html>`;
  }
}

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
