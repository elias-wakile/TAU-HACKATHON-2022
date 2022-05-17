import { Box, BoxProps, Input } from '@chakra-ui/react'
import { theme } from '../theme'

export const FileInput = ({ ...props }: BoxProps) => {
	return (
		<Box color={theme.defaultColor} data-id='FileInput' {...props}>
			<Input type={'file'}></Input>
		</Box>
	)
}
