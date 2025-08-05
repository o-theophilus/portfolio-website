<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { module } from '$lib/store.svelte.js';
	import { page } from '$app/state';

	import { Button, ButtonFold, Toggle } from '$lib/button';
	import Access_Ok from './_access.ok.svelte';
	import { Icon } from '$lib/macro';

	let { user = page.data.user } = $props();
	let init = [...user.access];
	let mods = $state([...user.access]);
	if (module.value.mods) {
		mods = [...module.value.mods];
	}
	let sub_open = $state('');

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

	{#each Object.entries(page.data.access) as [_type, level]}
		<div
			class="type"
			role="presentation"
			onclick={() => {
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
								onclick={() => {
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

	<div class="line">
		<Button
			disabled={mods.sort().join(',') == init.sort().join(',')}
			onclick={() => module.open(Access_Ok, { mods })}
		>
			Submit
			<Icon icon="send" />
		</Button>
		<Button
			disabled={mods.sort().join(',') == init.sort().join(',')}
			onclick={() => {
				mods = [...init];
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

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp1);
	}
</style>
