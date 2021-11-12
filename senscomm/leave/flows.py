from viewflow import flow, frontend
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView

from .models import LeaveProcess

@frontend.register
class LeaveFlow(Flow):
    process_class = LeaveProcess

    start = (
            flow.Start(
                CreateProcessView,
                fields=["reason"]
                ).Permission(
                    auto_create=True
                    ).Next(this.approve)
                )

    approve = (
            flow.View(
                UpdateProcessView,
                fields=["approved"]
                ).Permission(
                    auto_create=True
                    ).Next(this.check_approve)
                )

    check_approve = (
            flow.If(lambda activation: activation.process.approved)
            .Then(this.send)
            .Else(this.end)
            )

    send = (
            flow.Handler(
                this.send_leave_request
                ).Next(this.end)
            )

    end = flow.End()

    def send_leave_request(self, activation):
        print(activation.process.text)
