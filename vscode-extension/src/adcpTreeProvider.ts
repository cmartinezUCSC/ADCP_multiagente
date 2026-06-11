import * as vscode from 'vscode';
import { StateManager, AdcpPhase } from './stateManager';

export class AdcpTreeItem extends vscode.TreeItem {
  constructor(
    public readonly label: string,
    public readonly phase: AdcpPhase | null,
    collapsibleState: vscode.TreeItemCollapsibleState,
    public readonly command?: vscode.Command,
    isComplete?: boolean
  ) {
    super(label, collapsibleState);
    if (phase !== null) {
      this.iconPath = isComplete
        ? new vscode.ThemeIcon('pass', new vscode.ThemeColor('testing.iconPassed'))
        : new vscode.ThemeIcon('circle-large-outline');
      this.contextValue = isComplete ? 'phase-complete' : 'phase-pending';
      this.tooltip = isComplete ? `${label} — completado` : `${label} — pendiente`;
    }
  }
}

const PHASE_COMMANDS: Record<AdcpPhase, string> = {
  [AdcpPhase.Analyze]: 'adcp.analyze',
  [AdcpPhase.Design]: 'adcp.design',
  [AdcpPhase.Construct]: 'adcp.construct',
  [AdcpPhase.Test]: 'adcp.test',
};

export class AdcpTreeDataProvider
  implements vscode.TreeDataProvider<AdcpTreeItem>
{
  private _onDidChangeTreeData = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  constructor(private readonly stateManager: StateManager) {}

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  getTreeItem(element: AdcpTreeItem): vscode.TreeItem {
    return element;
  }

  getChildren(element?: AdcpTreeItem): AdcpTreeItem[] {
    if (element) {
      return [];
    }

    const projectName = this.stateManager.getProjectName();
    const items: AdcpTreeItem[] = [];

    if (projectName) {
      items.push(
        new AdcpTreeItem(
          `Proyecto: ${projectName}`,
          null,
          vscode.TreeItemCollapsibleState.None
        )
      );
    } else {
      items.push(
        new AdcpTreeItem(
          'Sin proyecto activo',
          null,
          vscode.TreeItemCollapsibleState.None
        )
      );
    }

    for (const phase of Object.values(AdcpPhase)) {
      const isComplete = this.stateManager.isPhaseComplete(phase);
      items.push(
        new AdcpTreeItem(
          phase,
          phase,
          vscode.TreeItemCollapsibleState.None,
          {
            command: PHASE_COMMANDS[phase],
            title: `Ejecutar ${phase}`,
          },
          isComplete
        )
      );
    }

    return items;
  }
}
