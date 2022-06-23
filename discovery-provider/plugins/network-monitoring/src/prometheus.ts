
import client from 'prom-client';

const PUSH_GATEWAY_URL = process.env['PUSH_GATEWAY_URL'] || 'https://localhost:9091'

export const gateway = new client.Pushgateway(PUSH_GATEWAY_URL)

export const allUserCountGauge = new client.Gauge({
    name: 'all_user_count',
    help: 'the count of users with this content node in their replica set',
    labelNames: ['endpoint', 'run_id'],
})

export const primaryUserCountGauge = new client.Gauge({
    name: 'primary_user_count',
    help: 'the count of users with this content node as their primary',
    labelNames: ['endpoint', 'run_id'],
})

export const fullySyncedUsersCountGauge = new client.Gauge({
    name: 'full_synced_user_count',
    help: 'the number of users whose content nodes replicas are all in sync',
    labelNames: ['run_id']
})
