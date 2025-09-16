; Script de Inno Setup para INE Transformer
; Genera un instalador MSI-like que reduce detecciones de antivirus

#define MyAppName "INE Transformer 4 E-Season"
#define MyAppVersion "4.1"
#define MyAppPublisher "Capfun Spain - David Arenas"
#define MyAppURL "https://github.com/dawnsystem/INE_2_e-season"
#define MyAppExeName "INE_4_e-season.exe"

[Setup]
; ID unico de la aplicacion
AppId={{A7B3C4D5-E6F7-8901-2345-6789ABCDEF01}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={autopf}\INE_Transformer
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; Carpeta de salida del instalador
OutputDir=installer
OutputBaseFilename=INE_Transformer_Setup_v{#MyAppVersion}
; Icono del instalador
SetupIconFile=logo_ine.ico
; Compresion
Compression=lzma2/max
SolidCompression=yes
; Version minima de Windows
MinVersion=6.1sp1
; Arquitectura
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
; Firma digital
SignTool=signtool
SignedUninstaller=yes
; Informacion
VersionInfoVersion={#MyAppVersion}.0.0
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Sistema de procesamiento de encuestas INE para E-Season
VersionInfoCopyright=Copyright 2024 David Arenas - MIT License
; Privilegios
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Ejecutable principal
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; Iconos
Source: "logo_ine.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "logo_ine.png"; DestDir: "{app}"; Flags: ignoreversion
; Documentacion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "SECURITY.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "docs\MANUAL_USUARIO_COMPLETO.md"; DestDir: "{app}\docs"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\logo_ine.ico"
Name: "{group}\Manual de Usuario"; Filename: "{app}\docs\MANUAL_USUARIO_COMPLETO.md"
Name: "{group}\Informacion de Seguridad"; Filename: "{app}\SECURITY.md"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\logo_ine.ico"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon; IconFilename: "{app}\logo_ine.ico"

[Run]
; Opcion para ejecutar al finalizar
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Limpiar archivos generados
Type: files; Name: "{app}\*.xlsx"
Type: files; Name: "{app}\historial_exportaciones.json"
Type: dirifempty; Name: "{app}"

[Code]
// Verificar si ya esta instalado
function InitializeSetup(): Boolean;
begin
  Result := True;
end;

// Mensaje post-instalacion
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox('Instalacion completada exitosamente.' + #13#10 + #13#10 +
           'Si tu antivirus detecta el programa como amenaza:' + #13#10 +
           '1. Es un FALSO POSITIVO comun con aplicaciones Python' + #13#10 +
           '2. Agrega la carpeta de instalacion a las exclusiones' + #13#10 +
           '3. Consulta SECURITY.md para mas informacion',
           mbInformation, MB_OK);
  end;
end;

[Registry]
; Registrar la aplicacion en Windows
Root: HKCU; Subkey: "Software\Capfun\INE_Transformer"; ValueType: string; ValueName: "Version"; ValueData: "{#MyAppVersion}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Capfun\INE_Transformer"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey

[CustomMessages]
spanish.LaunchProgram=Ejecutar %1 ahora
spanish.CreateDesktopIcon=Crear icono en el escritorio
spanish.CreateQuickLaunchIcon=Crear icono de inicio rapido