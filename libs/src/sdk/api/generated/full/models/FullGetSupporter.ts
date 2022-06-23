// @ts-nocheck
/* tslint:disable */
/* eslint-disable */
/**
 * API
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
import {
    FullSupporter,
    FullSupporterFromJSON,
    FullSupporterFromJSONTyped,
    FullSupporterToJSON,
} from './FullSupporter';
import {
    VersionMetadata,
    VersionMetadataFromJSON,
    VersionMetadataFromJSONTyped,
    VersionMetadataToJSON,
} from './VersionMetadata';

/**
 * 
 * @export
 * @interface FullGetSupporter
 */
export interface FullGetSupporter {
    /**
     * 
     * @type {number}
     * @memberof FullGetSupporter
     */
    latest_chain_block: number;
    /**
     * 
     * @type {number}
     * @memberof FullGetSupporter
     */
    latest_indexed_block: number;
    /**
     * 
     * @type {number}
     * @memberof FullGetSupporter
     */
    latest_chain_slot_plays: number;
    /**
     * 
     * @type {number}
     * @memberof FullGetSupporter
     */
    latest_indexed_slot_plays: number;
    /**
     * 
     * @type {string}
     * @memberof FullGetSupporter
     */
    signature: string;
    /**
     * 
     * @type {string}
     * @memberof FullGetSupporter
     */
    timestamp: string;
    /**
     * 
     * @type {VersionMetadata}
     * @memberof FullGetSupporter
     */
    version: VersionMetadata;
    /**
     * 
     * @type {FullSupporter}
     * @memberof FullGetSupporter
     */
    data?: FullSupporter;
}

export function FullGetSupporterFromJSON(json: any): FullGetSupporter {
    return FullGetSupporterFromJSONTyped(json, false);
}

export function FullGetSupporterFromJSONTyped(json: any, ignoreDiscriminator: boolean): FullGetSupporter {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'latest_chain_block': json['latest_chain_block'],
        'latest_indexed_block': json['latest_indexed_block'],
        'latest_chain_slot_plays': json['latest_chain_slot_plays'],
        'latest_indexed_slot_plays': json['latest_indexed_slot_plays'],
        'signature': json['signature'],
        'timestamp': json['timestamp'],
        'version': VersionMetadataFromJSON(json['version']),
        'data': !exists(json, 'data') ? undefined : FullSupporterFromJSON(json['data']),
    };
}

export function FullGetSupporterToJSON(value?: FullGetSupporter | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'latest_chain_block': value.latest_chain_block,
        'latest_indexed_block': value.latest_indexed_block,
        'latest_chain_slot_plays': value.latest_chain_slot_plays,
        'latest_indexed_slot_plays': value.latest_indexed_slot_plays,
        'signature': value.signature,
        'timestamp': value.timestamp,
        'version': VersionMetadataToJSON(value.version),
        'data': FullSupporterToJSON(value.data),
    };
}
