import * as vscode from 'vscode';
import { AdcpPanel } from './adcpPanel';
import { BackendClient } from './backendClient';
import { StateManager, AdcpPhase } from './stateManager';
import { AdcpTreeDataProvider } from './adcpTreeProvider';

let stateManager: StateManager;
let backendClient: BackendClient;

export function activate(context: vscode.ExtensionContext): void {
  stateManager = new StateManager(context.workspaceState);
  backendClient = new BackendClient();

  const treeProvider = new AdcpTreeDataProvider(stateManager);
  vscode.window.registerTreeDataProvider('adcpPhases', treeProvider);

  const config = vscode.workspace.getConfiguration('adcp');
  if (config.get<boolean>('autoStartBackend')) {
    backendClient.checkHealth().then((ok) => {
      if (!ok) {
        vscode.window.showInformationMessage('ADCP: Backend no disponible en ' + backendClient.baseUrl);
      }
    });
  }

  context.subscriptions.push(
    vscode.commands.registerCommand('adcp.analyze', () =>
      runPhase('analyze', AdcpPhase.Analyze, treeProvider)
    ),
    vscode.commands.registerCommand('adcp.design', () =>
      runPhase('design', AdcpPhase.Design, treeProvider)
    ),
    vscode.commands.registerCommand('adcp.construct', () =>
      runPhase('construct', AdcpPhase.Construct, treeProvider)
    ),
    vscode.commands.registerCommand('adcp.test', () =>
      runPhase('test', AdcpPhase.Test, treeProvider)
    ),
    vscode.commands.registerCommand('adcp.showPanel', () => {
      AdcpPanel.createOrShow(context.extensionUri, stateManager);
    }),
    vscode.commands.registerCommand('adcp.resetState', async () => {
      const confirm = await vscode.window.showWarningMessage(
        '¿Reiniciar todo el estado del proyecto ADCP?',
        { modal: true },
        'Sí'
      );
      if (confirm === 'Sí') {
        await stateManager.reset();
        treeProvider.refresh();
        vscode.window.showInformationMessage('ADCP: Estado reiniciado.');
      }
    }),
    vscode.commands.registerCommand('adcp.startBackend', async () => {
      const terminal = vscode.window.createTerminal({
        name: 'ADCP Backend',
        cwd: context.extensionUri.fsPath + '/../backend',
      });
      terminal.show();
      terminal.sendText('python3 -m uvicorn main:app --reload --port 8000');
    })
  );

  vscode.window.showInformationMessage('ADCP Multiagente activado. Use la barra lateral para comenzar.');
}

async function runPhase(
  endpoint: string,
  phase: AdcpPhase,
  treeProvider: AdcpTreeDataProvider
): Promise<void> {
  const projectName = await vscode.window.showInputBox({
    prompt: `Nombre o descripción del proyecto para la fase ${phase}`,
    placeHolder: 'Sistema de gestión de inventario...',
    value: stateManager.getProjectName() ?? '',
  });
  if (!projectName) {
    return;
  }

  await stateManager.setProjectName(projectName);

  const previousPhaseResult = getPreviousPhaseContext(phase);

  await vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: `ADCP: Ejecutando fase ${phase}...`,
      cancellable: false,
    },
    async () => {
      try {
        const result = await backendClient.runPhase(endpoint, {
          project_name: projectName,
          context: previousPhaseResult,
        });
        await stateManager.savePhaseResult(phase, result);
        treeProvider.refresh();
        AdcpPanel.createOrShow(
          vscode.Uri.file(''),  // placeholder; panel uses its own context
          stateManager
        );
        vscode.window.showInformationMessage(`ADCP: Fase ${phase} completada.`);
      } catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        vscode.window.showErrorMessage(`ADCP: Error en la fase ${phase}: ${message}`);
      }
    }
  );
}

function getPreviousPhaseContext(phase: AdcpPhase): string {
  switch (phase) {
    case AdcpPhase.Design:
      return stateManager.getPhaseResult(AdcpPhase.Analyze) ?? '';
    case AdcpPhase.Construct:
      return stateManager.getPhaseResult(AdcpPhase.Design) ?? '';
    case AdcpPhase.Test:
      return stateManager.getPhaseResult(AdcpPhase.Construct) ?? '';
    default:
      return '';
  }
}

export function deactivate(): void {
  // nothing to clean up
}
