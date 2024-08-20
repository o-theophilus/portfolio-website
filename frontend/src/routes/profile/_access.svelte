<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { module } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Toggle from '$lib/toggle.svelte';
	import ButtonFold from '$lib/button/fold.svelte';
	import Access_Ok from './_access.ok.svelte';
	import Icon from '$lib/icon.svelte';

	export let user = $module.user;
	let init = [...$module.user.access];
	let mods = [...$module.user.access];
	let sub_open = '';

	const select = (_in) => {
		if (mods.includes(_in)) {
			mods = mods.filter((x) => x != _in);
		} else {
			mods.push(_in);
			mods = mods;
		}
	};
</script>

<section>
	<strong class="ititle"> Edit Access </strong>

	{#each Object.entries($module.access) as [_type, level]}
		<div
			class="type"
			role="presentation"
			on:click={() => {
				if (sub_open == _type) {
					sub_open = '';
				} else {
					sub_open = _type;
				}
			}}
		>
			{_type}
			<ButtonFold open={sub_open == _type} />
		</div>
		{#if sub_open == _type}
			<div class="content" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
				{#each Object.entries(level) as [lv, actions]}
					<div class="sub_type">
						Level {lv}
					</div>

					<div class="access_area">
						{#each actions as ac}
							<Toggle
								state_1=""
								state_2={ac.split('_').join(' ')}
								active={mods.includes(`${_type}:${ac}`)}
								on:click={() => {
									select(`${_type}:${ac}`);
								}}
							/>
						{/each}
					</div>
				{/each}
			</div>
		{/if}
	{/each}

	<br />

	<div class="btns">
		<Button
			disabled={mods.sort().join(',') == init.sort().join(',')}
			on:click={() => {
				$module = {
					module: Access_Ok,
					key: user.key,
					access: mods
				};
			}}
		>
			Submit
			<Icon icon="send" />
		</Button>
		<Button
			disabled={mods.sort().join(',') == init.sort().join(',')}
			on:click={() => {
				mods = init;
			}}
		>
			Reset
			<Icon icon="history" />
		</Button>
	</div>
</section>

<style>
	section {
		padding: var(--sp3);
	}

	.type {
		display: flex;
		align-items: center;
		gap: var(--sp2);
		justify-content: space-between;

		padding: var(--sp1) 0;
		cursor: pointer;
		text-transform: capitalize;
		font-weight: 900;
	}

	.content {
		border: 0 solid var(--bg2);
		border-width: 1px 0;
		padding-bottom: var(--sp1);
	}

	.sub_type {
		font-weight: 900;
		font-size: 0.8rem;
		margin: var(--sp1) 0;
	}

	.access_area {
		display: flex;
		align-items: center;
		gap: var(--sp0);
		flex-wrap: wrap;

		margin: var(--sp0) 0;
	}

	.btns {
		display: flex;
		align-items: center;
		gap: var(--sp0);
	}
</style>
