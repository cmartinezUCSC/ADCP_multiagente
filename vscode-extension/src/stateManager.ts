import * as vscode from 'vscode';

export enum AdcpPhase {
  Analyze = 'Análisis',
  Design = 'Diseño',
  Construct = 'Construcción',
  Test = 'Pruebas',
}

const PHASE_KEYS: Record<AdcpPhase, string> = {
  [AdcpPhase.Analyze]: 'adcp.phase.analyze',
  [AdcpPhase.Design]: 'adcp.phase.design',
  [AdcpPhase.Construct]: 'adcp.phase.construct',
  [AdcpPhase.Test]: 'adcp.phase.test',
};

const PROJECT_NAME_KEY = 'adcp.projectName';

export class StateManager {
  constructor(private readonly workspaceState: vscode.Memento) {}

  getProjectName(): string | undefined {
    return this.workspaceState.get<string>(PROJECT_NAME_KEY);
  }

  async setProjectName(name: string): Promise<void> {
    await this.workspaceState.update(PROJECT_NAME_KEY, name);
  }

  getPhaseResult(phase: AdcpPhase): string | undefined {
    return this.workspaceState.get<string>(PHASE_KEYS[phase]);
  }

  async savePhaseResult(phase: AdcpPhase, result: string): Promise<void> {
    await this.workspaceState.update(PHASE_KEYS[phase], result);
  }

  getCompletedPhases(): AdcpPhase[] {
    return Object.values(AdcpPhase).filter(
      (phase) => this.getPhaseResult(phase) !== undefined
    );
  }

  isPhaseComplete(phase: AdcpPhase): boolean {
    return this.getPhaseResult(phase) !== undefined;
  }

  async reset(): Promise<void> {
    await this.workspaceState.update(PROJECT_NAME_KEY, undefined);
    for (const key of Object.values(PHASE_KEYS)) {
      await this.workspaceState.update(key, undefined);
    }
  }
}
