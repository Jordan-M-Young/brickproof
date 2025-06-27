x = {
    "metadata": {
        "job_id": 625234784902960,
        "run_id": 89018493834650,
        "creator_user_name": "jordan.m.young0@gmail.com",
        "number_in_job": 89018493834650,
        "original_attempt_run_id": 89018493834650,
        "state": {
            "life_cycle_state": "TERMINATED",
            "result_state": "FAILED",
            "state_message": "Workload failed, see run output for details",
            "user_cancelled_or_timedout": False,
        },
        "start_time": 1750956453277,
        "setup_duration": 4000,
        "execution_duration": 46000,
        "cleanup_duration": 0,
        "end_time": 1750956503990,
        "trigger": "ONE_TIME",
        "run_name": "brickproof-Unittests",
        "run_page_url": "***/?o=2567941339669575#job/625234784902960/run/89018493834650",
        "run_type": "JOB_RUN",
        "parent_run_id": 890553971536365,
        "tasks": [
            {
                "run_id": 89018493834650,
                "task_key": "brickproof-Unittests",
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/jordan.m.young0@gmail.com/.brickproof_testing/brickproof/brickproof_runner.py",
                    "source": "WORKSPACE",
                },
                "state": {
                    "life_cycle_state": "TERMINATED",
                    "result_state": "FAILED",
                    "state_message": "Workload failed, see run output for details",
                    "user_cancelled_or_timedout": False,
                },
                "run_page_url": "***/?o=2567941339669575#job/625234784902960/run/89018493834650",
                "start_time": 1750956453277,
                "setup_duration": 4000,
                "execution_duration": 46000,
                "cleanup_duration": 0,
                "end_time": 1750956503990,
                "attempt_number": 0,
                "status": {
                    "state": "TERMINATED",
                    "termination_details": {
                        "code": "RUN_EXECUTION_ERROR",
                        "type": "CLIENT_ERROR",
                        "message": "Workload failed, see run output for details",
                    },
                },
                "effective_performance_target": "PERFORMANCE_OPTIMIZED",
            }
        ],
        "task_key": "brickproof-Unittests",
        "format": "MULTI_TASK",
        "status": {
            "state": "TERMINATED",
            "termination_details": {
                "code": "RUN_EXECUTION_ERROR",
                "type": "CLIENT_ERROR",
                "message": "Workload failed, see run output for details",
            },
        },
        "job_run_id": 890553971536365,
        "effective_performance_target": "PERFORMANCE_OPTIMIZED",
    },
    "error": "AssertionError: The pytest invocation failed. See the log above for details.",
    "error_trace": "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n\u001b[0;31mAssertionError\u001b[0m                            Traceback (most recent call last)\nFile \u001b[0;32m<command-734922519609824>, line 17\u001b[0m\n\u001b[1;32m     15\u001b[0m sys\u001b[38;5;241m.\u001b[39mstdout \u001b[38;5;241m=\u001b[39m old_stdout\n\u001b[1;32m     16\u001b[0m \u001b[38;5;66;03m# Fail the cell execution if we have any test failures.\u001b[39;00m\n\u001b[0;32m---> 17\u001b[0m \u001b[38;5;28;01massert\u001b[39;00m retcode \u001b[38;5;241m==\u001b[39m \u001b[38;5;241m0\u001b[39m, \u001b[38;5;124m'\u001b[39m\u001b[38;5;124mThe pytest invocation failed. See the log above for details.\u001b[39m\u001b[38;5;124m'\u001b[39m\n\n\u001b[0;31mAssertionError\u001b[0m: The pytest invocation failed. See the log above for details.",
    "notebook_output": {},
}
print("DATA", x["error"])
print("DATA", x["error_trace"])
