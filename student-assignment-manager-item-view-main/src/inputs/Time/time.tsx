import { Grid, Input, GridProps, Box, InputProps } from '@chakra-ui/react'
import { useMemo, useState } from 'react'
import { theme } from '../../theme'

export interface ITime {
	minutes: number
	hours: number
}

interface ITimeProps extends GridProps {
	value: ITime
	onChangeHandler: (time: ITime) => void
}

export const Time = ({ value, onChangeHandler, ...props }: ITimeProps) => {
	const inputProps = useMemo(() => {
		return {
			w: '100%',
			h: '100%',
			type: 'number',
			backgroundColor: theme.defaultColor,
			color: '#606c6e',
			outline: '0 solid transparent',
			border: '0 solid transparent',
			fontSize: '40px',
			borderRadius: '4px',
			letterSpacing: '-0.4px',
			min: 0,
			textAlign: 'center',
		} as InputProps
	}, [])

	return (
		<Grid
			textAlign='center'
			fontSize='40px'
			height='60px'
			data-id='Time'
			width='180px'
			position='absolute'
			left='50%'
			top='250px'
			templateColumns='1fr 4px 1fr'
			transform='translateX(-54%)'
			gap={6}
			{...props}
		>
			<Input
				data-id='hours-input'
				{...inputProps}
				max={99}
				value={(value.hours < 10 ? '0' : '') + value.hours}
				onChange={(e) => {
					onChangeHandler({ ...value, hours: Math.min(Math.max(parseInt(e.target.value), 0), 99) })
				}}
			></Input>
			<Box color={theme.defaultColor} w='100%' textAlign='center'>
				:
			</Box>
			<Input
				data-id='minutes-input'
				{...inputProps}
				max={59}
				value={(value.minutes < 10 ? '0' : '') + value.minutes}
				onChange={(e) => {
					onChangeHandler({
						...value,
						minutes: Math.min(Math.max(parseInt(e.target.value), 0), 59),
					})
				}}
			></Input>
		</Grid>
	)
}
