
{% if data['body'] is defined %}
{% set body_json = data['body']|load_json %}
{% set metric = body_json['evalMatches'][0]['metric'] %}
{% set metric_split = metric.split(' ') %}
{% set device = metric_split[-1] %}
{% set val = body_json['evalMatches'][0]['value'] %}
{% set alertname = body_json['ruleName'] %}
{% set state = body_json['state'] %}
{% endif %}

create_a_new_ticket_or_update_the_existing_one:
    runner.request_tracker.create_ticket:
        - args:
            subject: "Alert from Grafana - Alert name is '{{ alertname }} - {{ metric }}"
            text: "State: {{ state }} - Number of ESTABLISHED BGP sessions is '{{ val }}'"















