# fakeE2EBlackbox

This is for experimenting with Prometheus on OpenShift

This repo and the scripts (well commands) below will deploy a small Prometheus infrastructure,
suitable for experiment, to any OpenShift you have access to.   I strongly recommend 'minishift'
if you don't have access to an OpenShift you like better.

The scripts will deploy a Prometheus service along with an Alertmanager service.  It also deploys
a tiny python app, called fake-e2e-blackbox, for the Prometheus server to monitor.  This python
app pretends to be a blackbox end-to-end test of some other service, and presents the results such
that Prometheus can monitor them.   It pretends by generating fuzzy (random within controlled bounds)
test results.

The deployed Prometheus service is configured to monitor the fake-e2e-blackbox app.  It is also
configured to alert, through the deployed Alertmanager, if the test results fall below a 90%
success rate.

The fake-e2e-blackbox app is configured to produce fuzzy results around 93% successful for 1.5 minutes
after starting, then around 1% for 5 minutes, then return to 94% forever.

The Alertmanager deployment is just configured to notice the alerts.  It can be, and has been,
configured to report alerts to Slack, but that requires a security token that I won't push to a
public repo.

The result of the above is that once deployed, you can bring up the Alertmanager frontend in a
browser, after about 1.5 minutes after the fake-e2e-blackbox app starts, two alerts will shop up
in Alertmanager.

You can also bring up the Prometheus frontend and play with that.

You can also do http GETs directly to the fake-e2e-blackbox app to see the metrics data that it
is presenting to Prometheus.

You can also edit the scripts and the app itself to play around.

-------------------------------------------------------------------------------------------

First checkout a copy of this repo.  The scripts must be run locally on your development
machine.

Second log into your favorite OpenShift instance.  Again I recomend 'minishift' if you don't
already have something you like better.

Third, I strongly recommend you create your own project to do this.  It really helps keep this
work separate from any other works.

    MYPROJECT=$(oc whoami)-fake-e2e-project
    oc new-project $MYPROJECT

oc status' is your friend, use it early and often.

cd to the top level of your checked out copy of this repo.  This README should be in that directory.

    oc create -f fake-e2e-blackbox-deploy.yml -f prometheus-deploy.yml -f alertmanager-deploy.yml
    oc status

Repeat 'oc status' till it reports three different pods deployed.  If it seems to fail in some way
see below for some trouble shooting tools

'oc status' shows threee URLs, one for fake-e2e-blackbox, one for prometheus, and one for alertmanager.
Browse to any or all of them to see what's going on in each of these.

'oc get all,cm' will show all the resources created by these 'scripts'.

'oc get -o yaml <resorcetype/resourcename>' will get a detailed yaml report on the current state of
any resource.  So 'oc get -o yaml dc/fake-e2e-blackbox' gets a detailed yaml report of the
fake-e2e-blackbox deployment config.

'oc describe <resorcetype/resourcename>' will give human readable description of resource.

'oc logs <resorcetype/resourcename>' will print out any logs produced by that resource.

To delete all the resources created by these scripts:

    oc delete -f fake-e2e-blackbox-deploy.yml -f prometheus-deploy.yml -f alertmanager-deploy.yml

To change any of the resorces, for example to change the configuration for prometheus or alertmanager,
edit the yaml files in your checked out copy of this repo, then

    oc delete -f fake-e2e-blackbox-deploy.yml -f prometheus-deploy.yml -f alertmanager-deploy.yml
    oc create -f fake-e2e-blackbox-deploy.yml -f prometheus-deploy.yml -f alertmanager-deploy.yml

There is probably a more elegant way to do this, but I like the certanty of rebooting.

To change the fake-e2e-blackbox app, edit the python script in your checked out copy of this repo,
then from the top level (where this README is):

    oc start-build bc/fake-e2e-blackbox --from-dir=./fakeE2EBlackbox/

This will build a new version of the app, with your changes, and deploy it.  Prometheus will show
a short gap of results while the pod is replaced, and then show result of your changes.

You may want to delete your project when your done:

    oc delete project $MYPROJECT


