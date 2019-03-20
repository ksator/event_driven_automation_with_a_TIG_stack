{% set bgp_response = salt['junos.rpc']('get-bgp-summary-information', '','json') %}
{% for peer in bgp_response['rpc_reply']['bgp-information'][0]['bgp-peer'] %}
validate_bgp_session_state_with_{{ peer['peer-address'][0]['data'] }}:
  loop.until:
    - name: junos.rpc
    - condition: m_ret['rpc_reply']['bgp-information']['bgp-peer']['peer-state'] == 'Established'
    - period: 5
    - timeout: 20
    - m_args:
      - get-bgp-neighbor-information
    - m_kwargs:
        neighbor-address: {{ peer['peer-address'][0]['data'] }}
{% endfor %}

