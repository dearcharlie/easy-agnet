// Prevents additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::{Child, Command};
use std::sync::{Arc, Mutex};

struct HermesProcess(Arc<Mutex<Option<Child>>>);

#[tauri::command]
fn start_hermes(state: tauri::State<HermesProcess>) -> Result<String, String> {
    let mut proc = state.0.lock().map_err(|e| e.to_string())?;

    if proc.is_some() {
        return Ok("Hermes API Server is already running".to_string());
    }

    let child = Command::new("hermes")
        .args(["api", "--port", "8520"])
        .spawn()
        .map_err(|e| format!("Failed to start Hermes API Server: {}", e))?;

    *proc = Some(child);
    Ok("Hermes API Server started on 127.0.0.1:8520".to_string())
}

#[tauri::command]
fn stop_hermes(state: tauri::State<HermesProcess>) -> Result<String, String> {
    let mut proc = state.0.lock().map_err(|e| e.to_string())?;

    match proc.take() {
        Some(mut child) => {
            child.kill().map_err(|e| format!("Failed to stop: {}", e))?;
            child.wait().ok();
            Ok("Hermes API Server stopped".to_string())
        }
        None => Ok("No Hermes process running".to_string()),
    }
}

#[tauri::command]
async fn check_hermes_health() -> Result<String, String> {
    reqwest::get("http://127.0.0.1:8520/health")
        .await
        .map(|r| {
            if r.status().is_success() {
                "connected".to_string()
            } else {
                "error".to_string()
            }
        })
        .map_err(|_| "disconnected".to_string())
}

fn main() {
    let process = Arc::new(Mutex::new(None));
    let close_process = process.clone();

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(HermesProcess(process))
        .invoke_handler(tauri::generate_handler![
            start_hermes,
            stop_hermes,
            check_hermes_health,
        ])
        .on_window_event(move |_window, event| {
            if let tauri::WindowEvent::CloseRequested { .. } = event {
                if let Ok(mut proc) = close_process.lock() {
                    if let Some(mut child) = proc.take() {
                        child.kill().ok();
                        child.wait().ok();
                    }
                }
            }
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
