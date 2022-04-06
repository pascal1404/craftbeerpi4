import asyncio
import json
from cbpi.api import parameters, Property, CBPiActor
from cbpi.api import *

@parameters([Property.Text(label="Topic", configurable=True, description = "MQTT Topic"),
             Property.Select(label="delay_type", options=["switch-on delay","switch-off delay"],description="Should the delay influence the switch-off or the switch-on process"),
             Property.Select(label="break", options=["paused","reset"],description="decide what happend if you press the button while delaytime runs"),
             Property.Select(label="direct_start", options=["Yes", "No"],description="If set to 'Yes' delay time will start direcly after button press"),
             Property.Number(label="delay_time", configurable=True,description="Time in seconds of the delay")])
class MQTTTimedActor(CBPiActor):

    def __init__(self, cbpi, id, props):
        super(MQTTTimedActor, self).__init__(cbpi, id, props)

    async def on_start(self):
        self.topic = self.props.get("Topic", None)
        self.swOffDelay = True if self.props.get("delay_type", "switch-off delay") == "switch-off delay" else False
        self.reset = True if self.props.get("break", "paused") == "reset" else False
        self.direct = True if self.props.get("direct_start", "No") == "Yes" else False
        self.delayTime = int(self.props.get("delay_time", 5))
        self.timer = 0
        self.power = 100
        self.reqstate = False
        self.state = False
        self.first = True
        self.paused = False

    async def on(self, power=0):
        if self.swOffDelay == True:
            self.timer = self.delayTime
            await self.cbpi.satellite.publish(self.topic, json.dumps(
                    {"state": "on", "power": self.power, "timer": self.timer}), True)
            self.state = True
            await self.cbpi.actor.timeractor_update(self.id, self.timer)
        else:
            if self.timer > 0:
                if self.reset:
                    self.timer = 0
                    self.reqstate = False
                    await self.cbpi.actor.timeractor_update(self.id, self.timer)
                    return ;
                else:
                    self.paused = not self.paused
        self.reqstate = True

    async def off(self):
        if self.swOffDelay == False:
            self.timer = 0
            await self.cbpi.satellite.publish(self.topic, json.dumps(
                    {"state": "off", "power": self.power, "timer": self.timer}), True)
            self.state = False
            await self.cbpi.actor.timeractor_update(self.id, self.timer)
        else:
            if self.timer < self.delayTime:
                if self.reset:
                    self.timer = self.delayTime
                    self.reqstate = True
                    await self.cbpi.actor.timeractor_update(self.id, self.timer)
                    return ;
                else:
                    self.paused = not self.paused
        self.reqstate = False

    def get_state(self):
        return self.state
    
    async def run(self):
        while self.running == True:
            if self.direct:
                if self.swOffDelay == False and not self.paused:
                    if self.timer < self.delayTime:
                        self.timer += 1
                        await self.cbpi.actor.timeractor_update(self.id, self.timer)
                        await self.cbpi.satellite.publish(self.topic, json.dumps(
                                {"state": "off", "power": self.power, "timer": self.timer}), True)
                        await asyncio.sleep(1)
                        self.first = True
                    else:
                        self.state = True
                        if self.first:
                            self.first = False
                            await self.cbpi.satellite.publish(self.topic, json.dumps(
                                    {"state": "on", "power": self.power, "timer": self.timer}), True)
                            await self.cbpi.actor.timeractor_update(self.id, self.timer)
                        await asyncio.sleep(1)
                elif self.swOffDelay == True and not self.paused:
                    if self.timer > 0:
                        self.timer -= 1
                        await self.cbpi.actor.timeractor_update(self.id, self.timer)
                        await self.cbpi.satellite.publish(self.topic, json.dumps(
                                {"state": "on", "power": self.power, "timer": self.timer}), True)
                        await asyncio.sleep(1)
                        self.first = True
                    else:
                        self.state = False
                        if self.first:
                            self.first = False
                            await self.cbpi.satellite.publish(self.topic, json.dumps(
                                    {"state": "off", "power": self.power, "timer": self.timer}), True)
                            await self.cbpi.actor.timeractor_update(self.id, self.timer)
                        await asyncio.sleep(1)
                else:
                    await asyncio.sleep(1)
            else:
                if self.reqstate == True:
                    if self.swOffDelay == False and not self.paused:
                        if self.timer < self.delayTime:
                            self.timer += 1
                            await self.cbpi.actor.timeractor_update(self.id, self.timer)
                            await self.cbpi.satellite.publish(self.topic, json.dumps(
                                    {"state": "off", "power": self.power, "timer": self.timer}), True)
                            await asyncio.sleep(1)
                            self.first = True
                        else:
                            self.state = True
                            if self.first:
                                self.first = False
                                await self.cbpi.satellite.publish(self.topic, json.dumps(
                                        {"state": "on", "power": self.power, "timer": self.timer}), True)
                                await self.cbpi.actor.timeractor_update(self.id, self.timer)
                            await asyncio.sleep(1)
                    else:
                        await asyncio.sleep(1)
                else:
                    if self.swOffDelay == True and not self.paused:
                        if self.timer > 0:
                            self.timer -= 1
                            await self.cbpi.actor.timeractor_update(self.id, self.timer)
                            await self.cbpi.satellite.publish(self.topic, json.dumps(
                                    {"state": "on", "power": self.power, "timer": self.timer}), True)
                            await asyncio.sleep(1)
                            self.first = True
                        else:
                            self.state = False
                            if self.first:
                                self.first = False
                                await self.cbpi.satellite.publish(self.topic, json.dumps(
                                        {"state": "off", "power": self.power, "timer": self.timer}), True)
                                await self.cbpi.actor.timeractor_update(self.id, self.timer)
                            await asyncio.sleep(1)
                    else:
                        await asyncio.sleep(1)